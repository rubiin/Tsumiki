from __future__ import annotations

import json
import os
import shlex
from contextlib import suppress
from time import monotonic

from fabric.utils import (
    GdkPixbuf,
    exec_shell_command,
    exec_shell_command_async,
    idle_add,
    logger,
)
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow

import utils.functions as helpers
from shared.circle_image import CircularImage
from shared.mixins import PopoverMixin
from shared.widget_container import ButtonWidget
from utils.functions import get_http_client
from utils.icons import get_text_icon
from utils.widget_utils import nerd_font_icon


def _load_pixbuf_from_bytes(image_bytes: bytes, size: int):
    loader = GdkPixbuf.PixbufLoader()
    loader.write(image_bytes)
    loader.close()

    pixbuf = loader.get_pixbuf()
    if pixbuf is None:
        return None

    return pixbuf.scale_simple(size, size, GdkPixbuf.InterpType.BILINEAR)


class GitHubClient:
    """Small GitHub API client for public repo and profile data."""

    def __init__(self, config: dict):
        self.config = config
        self.username = str(config.get("username", "Thomas-Philippot")).strip()
        self.repository = str(
            config.get("repository", "Thomas-Philippot/removarr-with-angular")
        ).strip()
        self.token = helpers.expand_env(
            str(config.get("token") or os.environ.get("GITHUB_TOKEN", ""))
        )

    @property
    def repo_owner(self) -> str:
        if "/" in self.repository:
            return self.repository.split("/", 1)[0]
        return self.username

    @property
    def repo_url(self) -> str:
        return f"https://github.com/{self.repository}" if self.repository else ""

    @property
    def profile_url(self) -> str:
        return f"https://github.com/{self.username}" if self.username else ""

    def _run_gh_api(self, endpoint: str, params: dict | None = None) -> dict | list:
        command_parts = ["gh", "api", endpoint, "--jq", ".", "-X", "GET"]
        if params:
            for key, value in params.items():
                command_parts.extend(["-f", f"{key}={value}"])

        cmd_str = " ".join(shlex.quote(p) for p in command_parts)
        old_token = os.environ.get("GH_TOKEN")
        try:
            if self.token:
                os.environ["GH_TOKEN"] = self.token

            result = exec_shell_command(cmd_str)
            if result is False:
                return {}
            payload = result.strip()
            if not payload:
                return {}
            return json.loads(payload)
        except Exception:
            return {}
        finally:
            if old_token is None:
                os.environ.pop("GH_TOKEN", None)
            else:
                os.environ["GH_TOKEN"] = old_token

    def fetch_state(self, avatar_size: int) -> dict:
        profile = {
            "name": self.username,
            "bio": "No bio",
            "avatar_url": "",
            "html_url": self.profile_url,
        }
        issues: list[dict] = []
        pulls: list[dict] = []

        with suppress(Exception):
            profile_data = self._run_gh_api("user")
            if isinstance(profile_data, dict):
                profile["name"] = profile_data.get("name") or profile_data.get(
                    "login", self.username
                )
                profile["bio"] = profile_data.get("bio") or "No bio"
                profile["avatar_url"] = profile_data.get("avatar_url", "")
                profile["html_url"] = profile_data.get("html_url") or self.profile_url

        if profile.get("avatar_url") == "":
            with suppress(Exception):
                profile_data = self._run_gh_api(f"users/{self.username}")
                if isinstance(profile_data, dict):
                    profile["avatar_url"] = profile_data.get("avatar_url", "")
                    profile["html_url"] = (
                        profile_data.get("html_url") or self.profile_url
                    )

        with suppress(Exception):
            repo_data = self._run_gh_api(f"repos/{self.repository}")
            if isinstance(repo_data, dict):
                profile["repo_full_name"] = repo_data.get("full_name", self.repository)
                profile["repo_description"] = repo_data.get("description", "") or ""

        with suppress(Exception):
            issues_data = self._run_gh_api(
                f"repos/{self.repository}/issues",
                params={"state": "open", "per_page": 100, "sort": "created"},
            )
            if isinstance(issues_data, list):
                issues = [
                    {**item, "kind": "issue"}
                    for item in issues_data
                    if isinstance(item, dict) and "pull_request" not in item
                ]

        with suppress(Exception):
            pulls_data = self._run_gh_api(
                f"repos/{self.repository}/pulls",
                params={"state": "open", "per_page": 100, "sort": "created"},
            )
            if isinstance(pulls_data, list):
                pulls = [
                    {**item, "kind": "pull_request"}
                    for item in pulls_data
                    if isinstance(item, dict)
                ]

        avatar_pixbuf = None
        avatar_url = str(profile.get("avatar_url", "")).strip()
        if avatar_url:
            with suppress(Exception):
                avatar_response = get_http_client().get(avatar_url, timeout=8)
                avatar_pixbuf = _load_pixbuf_from_bytes(
                    avatar_response.content,
                    avatar_size,
                )

        return {
            "profile": profile,
            "issues": issues,
            "pull_requests": pulls,
            "avatar_pixbuf": avatar_pixbuf,
        }


class GitCompanionPopoverContent(Box):
    """Popover content that matches the Git Companion preview."""

    def __init__(self, config: dict, parent=None, **kwargs):
        self.widget_config = config
        self.config = config
        self.client = GitHubClient(self.config)
        self.avatar_size = int(self.config.get("avatar_size", 44))
        self.default_tab = str(self.config.get("default_tab", "issues")).strip()
        self.cache_ttl = int(self.config.get("cache_ttl", 300))
        self._last_refresh_at = 0.0
        self._request_generation = 0
        self._active_tab = self._normalize_tab(self.default_tab)
        self._state: dict = {
            "profile": {
                "name": self.client.username,
                "bio": "No bio",
                "avatar_url": "",
                "html_url": self.client.profile_url,
            },
            "issues": [
                {
                    "title": "test issue",
                    "html_url": self.client.repo_url,
                    "repository_url": self.client.repo_url,
                    "number": 1,
                    "repository": self.client.repository,
                    "subtitle": f"{self.client.repository}#1",
                }
            ],
            "pull_requests": [],
            "avatar_pixbuf": None,
        }

        super().__init__(
            name="git-companion-window",
            orientation="v",
            spacing=10,
            **kwargs,
        )
        self._parent = parent

        self._build_ui()
        self._apply_state()
        self.refresh(force=True)

    def _normalize_tab(self, tab: str) -> str:
        return tab if tab in {"issues", "pull_requests"} else "issues"

    def _build_ui(self):
        self.header = Box(
            name="git-companion-header",
            orientation="h",
            h_expand=True,
            spacing=8,
        )

        self.title_box = Box(
            orientation="h",
            spacing=8,
            h_expand=True,
            children=[
                nerd_font_icon(
                    icon="",
                    props={"style_classes": ["git-companion-brand"]},
                ),
                Label(
                    label="Git Companion",
                    style_classes=["git-companion-title"],
                    h_align="start",
                ),
            ],
        )

        self.header_actions = Box(
            orientation="h",
            spacing=6,
            h_align="end",
            children=[
                self._make_action_button(
                    get_text_icon("ui.refresh"),
                    "Refresh",
                    self._on_refresh_clicked,
                ),
                self._make_action_button(
                    "",
                    "Open repository",
                    self._on_repo_clicked,
                ),
            ],
        )

        self.header.children = [self.title_box, self.header_actions]

        self.profile_card = Box(
            name="git-companion-profile",
            orientation="h",
            spacing=10,
            children=[],
        )

        self.avatar_box = Box(
            name="git-companion-avatar-box",
            style_classes=["git-companion-avatar-box"],
            size_request=(self.avatar_size, self.avatar_size),
        )

        self.profile_text = Box(
            orientation="v",
            spacing=2,
            h_expand=True,
            children=[
                Label(
                    label=self.client.username,
                    style_classes=["git-companion-name"],
                    h_align="start",
                ),
                Label(
                    label="No bio",
                    style_classes=["git-companion-bio"],
                    h_align="start",
                ),
            ],
        )
        self.profile_card.children = [self.avatar_box, self.profile_text]

        self.tabs = Box(
            name="git-companion-tabs",
            orientation="h",
            spacing=0,
            children=[
                self._make_tab_button("issues", "Issues (0)"),
                self._make_tab_button("pull_requests", "Pull Requests (0)"),
            ],
        )

        self.items_box = Box(
            name="git-companion-items",
            orientation="v",
            spacing=8,
            v_expand=True,
            h_expand=True,
        )

        self.scrolled = ScrolledWindow(
            name="git-companion-scroller",
            h_scrollbar_policy="never",
            v_scrollbar_policy="automatic",
            child=self.items_box,
        )
        self.scrolled.set_min_content_height(420)

        self.children = [
            self.header,
            self.profile_card,
            self.tabs,
            self.scrolled,
        ]

        self.name_label = self.profile_text.get_children()[0]
        self.bio_label = self.profile_text.get_children()[1]

    def _make_action_button(self, icon: str, tooltip: str, callback):
        return Button(
            name="git-companion-action-btn",
            style_classes=["git-companion-action-btn"],
            child=nerd_font_icon(
                icon=icon,
                props={"style_classes": ["git-companion-action-icon"]},
            ),
            tooltip_text=tooltip,
            on_clicked=callback,
        )

    def _make_tab_button(self, tab: str, label: str):
        button = Button(
            name=f"git-companion-tab-{tab}",
            style_classes=["git-companion-tab-btn"],
            child=Label(label=label, style_classes=["git-companion-tab-label"]),
            on_clicked=lambda *_: self.set_tab(tab),
        )
        button._tab_name = tab  # type: ignore[attr-defined]
        return button

    def _on_refresh_clicked(self, *_):
        self.refresh(force=True)

    def _on_repo_clicked(self, *_):
        target = self.client.repository or self.client.repo_url
        if target:
            exec_shell_command_async(f"gh repo view {shlex.quote(target)} --web")

    def _set_tab_button_state(self):
        for button in self.tabs.get_children():
            tab_name = getattr(button, "_tab_name", None)
            button.set_style_classes(
                ["git-companion-tab-btn", "active"]
                if tab_name == self._active_tab
                else ["git-companion-tab-btn"]
            )

    def _update_tab_labels(self):
        issues_count = len(self._state.get("issues", []))
        pulls_count = len(self._state.get("pull_requests", []))

        for button in self.tabs.get_children():
            tab_name = getattr(button, "_tab_name", None)
            label = button.get_child()
            if not isinstance(label, Label):
                continue
            if tab_name == "issues":
                label.set_label(f"Issues ({issues_count})")
            elif tab_name == "pull_requests":
                label.set_label(f"Pull Requests ({pulls_count})")

    def set_tab(self, tab: str):
        self._active_tab = self._normalize_tab(tab)
        self._set_tab_button_state()
        self._render_items()

    def _set_avatar(self, pixbuf):
        if pixbuf is None:
            self.avatar_box.children = [
                Box(
                    name="git-companion-avatar-fallback",
                    orientation="v",
                    h_align="center",
                    v_align="center",
                    children=[
                        nerd_font_icon(
                            icon="",
                            props={
                                "style_classes": ["git-companion-avatar-fallback-icon"]
                            },
                        )
                    ],
                )
            ]
            return

        self.avatar_box.children = [
            CircularImage(
                pixbuf=pixbuf,
                size=self.avatar_size,
                name="git-companion-avatar",
            )
        ]

    def _apply_state(self):
        profile = self._state.get("profile", {})
        self.name_label.set_label(str(profile.get("name", self.client.username)))
        bio_text = str(profile.get("bio", "No bio") or "No bio")
        if len(bio_text) > 30:
            bio_text = f"{bio_text[:29].rstrip()}…"
        self.bio_label.set_label(bio_text)
        self._set_avatar(self._state.get("avatar_pixbuf"))
        self._set_tab_button_state()
        self._update_tab_labels()
        self._render_items()

    def _truncate_text(self, text: str, max_length: int = 30) -> str:
        if len(text) <= max_length:
            return text
        return f"{text[: max_length - 1].rstrip()}…"

    def _normalize_description(self, text: str) -> str:
        normalized = str(text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
        if not normalized:
            return ""

        lines = [line.strip() for line in normalized.split("\n") if line.strip()]
        if not lines:
            return ""

        excerpt = "\n".join(lines[:2])
        if len(excerpt) > 140:
            excerpt = f"{excerpt[:139].rstrip()}…"

        return excerpt

    def _make_item_button(self, item: dict):
        title = self._truncate_text(str(item.get("title", "Untitled")).strip())
        subtitle = str(
            item.get("subtitle")
            or (
                f"{item.get('repository', self.client.repository)}"
                f"#{item.get('number', '')}"
            )
        ).strip()
        description = self._normalize_description(
            item.get("body") or item.get("description")
        )
        number = str(item.get("number", "")).strip()
        kind = str(item.get("kind", "issue"))
        command = (
            f"gh pr view {shlex.quote(number)} --repo "
            f"{shlex.quote(self.client.repository)} --web"
            if kind == "pull_request"
            else f"gh issue view {shlex.quote(number)} --repo "
            f"{shlex.quote(self.client.repository)} --web"
        )

        item_children = [
            Label(
                label=title,
                style_classes=["git-companion-item-title"],
                h_align="start",
            ),
            Label(
                label=subtitle,
                style_classes=["git-companion-item-subtitle"],
                h_align="start",
            ),
        ]

        if description:
            description_label = Label(
                label=description,
                style_classes=["git-companion-item-description"],
                h_align="start",
                line_wrap="word-char",
                max_chars_width=34,
            )
            description_label.set_lines(2)
            description_label.set_ellipsize(3)
            item_children.append(description_label)

        item_box = Box(
            orientation="v",
            spacing=1,
            children=item_children,
        )

        return Button(
            name="git-companion-item",
            style_classes=["git-companion-item"],
            child=item_box,
            on_clicked=(lambda *_: exec_shell_command_async(command))
            if number
            else None,
        )

    def _render_items(self):
        items = self._state.get(self._active_tab, [])
        if not isinstance(items, list):
            items = []

        self.items_box.children = [self._make_item_button(item) for item in items]

    @helpers.run_in_thread
    def _refresh_async(self, generation: int):
        try:
            state = self.client.fetch_state(self.avatar_size)
            idle_add(self._apply_refresh_result, generation, state)
        except Exception as error:
            logger.warning(f"[GitCompanion] Refresh failed: {error}")
            idle_add(self._mark_refresh_complete, generation)

    def _apply_refresh_result(self, generation: int, state: dict):
        if generation != self._request_generation:
            return False

        self._state.update(state)
        self._last_refresh_at = monotonic()
        self._apply_state()
        return False

    def _mark_refresh_complete(self, generation: int):
        if generation != self._request_generation:
            return False
        self._last_refresh_at = 0.0
        return False

    def _is_cache_valid(self) -> bool:
        if self.cache_ttl <= 0 or self._last_refresh_at <= 0:
            return False

        return (monotonic() - self._last_refresh_at) < self.cache_ttl

    def refresh(self, force: bool = False):
        if not force and self._is_cache_valid():
            return

        self._request_generation += 1
        generation = self._request_generation
        self._refresh_async(generation)


class GitCompanionWidget(ButtonWidget, PopoverMixin):
    """Bar button that opens Git Companion popup."""

    def __init__(self, **kwargs):
        super().__init__(name="git_companion", **kwargs)

        self.container_box.children = nerd_font_icon(
            icon=self.config.get("icon", ""),
            props={"style_classes": ["panel-font-icon"]},
        )

        if self.config.get("label", False):
            self.container_box.add(
                Label(
                    label=self.config("label_text", "Git"), style_classes=["panel-text"]
                )
            )

        if self.config.get("tooltip", True) and self.tooltips_enabled:
            self.set_tooltip_text(self.config.get("tooltip_text", "Open Git Companion"))

        self.setup_popover(
            lambda: GitCompanionPopoverContent(config=self.config, parent=self),
            connect_clicked=False,
        )
        self.connect("clicked", self.on_click)

    def on_click(self, *_):
        self.toggle_popover()

    def toggle_popover(self) -> None:
        popup = self.popup
        if popup and hasattr(popup, "content") and hasattr(popup.content, "refresh"):
            popup.content.refresh(force=False)
        super().toggle_popover()
