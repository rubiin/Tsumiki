from __future__ import annotations

import json
from typing import ClassVar
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from fabric.utils import GLib, idle_add, logger
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label

from shared.mixins import PopoverMixin
from shared.widget_container import ButtonWidget
from utils.functions import run_in_thread
from utils.widget_utils import nerd_font_icon


class CryptoMarketPopoverContent(Box):
    """Crypto market popup styled after legacy-v4 plugin preview."""

    _COIN_IDS: ClassVar[dict[str, str]] = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "BNB": "binancecoin",
        "SOL": "solana",
        "XRP": "ripple",
    }

    _COIN_ICONS: ClassVar[dict[str, str]] = {
        "BTC": "₿",
        "ETH": "◆",
        "BNB": "⬡",
        "SOL": "◈",
        "XRP": "✕",
    }

    def _log(self, message: str, *args):
        logger.warning(message, *args)

    def __init__(self, config: dict, parent=None, **kwargs):
        super().__init__(
            name="crypto-market-window",
            orientation="v",
            spacing=8,
            **kwargs,
        )

        self._parent = parent
        self._config = config.get("widgets", {}).get("crypto_market", {})
        self._request_generation = 0
        self._timer_id: int | None = None

        interval = int(self._config.get("refresh_interval", 5))
        self._refresh_interval = max(1, min(60, interval))
        self._red_rises = bool(self._config.get("red_rises", False))

        raw_coins = self._config.get("watch_list", ["BTC", "ETH", "BNB", "SOL", "XRP"])
        self._coins = [
            str(c).upper() for c in raw_coins if str(c).upper() in self._COIN_IDS
        ]
        if not self._coins:
            self._coins = ["BTC", "ETH", "BNB", "SOL", "XRP"]

        self._market_data: dict[str, dict] = {}

        self._log(
            "[crypto_market] init interval=%ss coins=%s endpoint=%s",
            self._refresh_interval,
            self._coins,
            self._config.get("endpoint", "https://api.coingecko.com/api/v3/simple/price"),
        )

        self._build_ui()
        self.refresh(force=True)

        self._timer_id = GLib.timeout_add(self._refresh_interval * 1000, self._tick)
        self.connect("destroy", self._on_destroy)

    def _build_ui(self):
        title = Label(
            label="Crypto Market",
            style_classes=["crypto-market-title"],
            h_align="start",
        )
        self.subtitle = Label(
            label=f"Refresh:{self._refresh_interval} seconds",
            style_classes=["crypto-market-subtitle"],
            h_align="start",
        )

        left_header = Box(
            orientation="v",
            spacing=0,
            h_expand=True,
            children=[title, self.subtitle],
        )

        self.btn_refresh = Button(
            name="crypto-market-action-refresh",
            style_classes=["crypto-market-action-btn"],
            child=nerd_font_icon(
                icon="",
                props={"style_classes": ["crypto-market-action-icon"]},
            ),
            on_clicked=self._on_refresh_click,
        )

        self.btn_settings = Button(
            name="crypto-market-action-settings",
            style_classes=["crypto-market-action-btn"],
            child=nerd_font_icon(
                icon="",
                props={"style_classes": ["crypto-market-action-icon"]},
            ),
        )

        self.btn_close = Button(
            name="crypto-market-action-close",
            style_classes=["crypto-market-action-btn", "danger"],
            child=nerd_font_icon(
                icon="",
                props={"style_classes": ["crypto-market-action-icon"]},
            ),
            on_clicked=self.close,
        )

        right_header = Box(
            orientation="h",
            spacing=6,
            children=[self.btn_refresh, self.btn_settings, self.btn_close],
        )

        self.header = Box(
            name="crypto-market-header",
            orientation="h",
            spacing=8,
            children=[left_header, right_header],
        )

        self.table_header = Box(
            name="crypto-market-table-header",
            orientation="h",
            spacing=10,
            children=[
                Label(label="Coin", style_classes=["crypto-market-th", "coin"]),
                Label(label="Price", style_classes=["crypto-market-th", "price"]),
                Label(label="Change", style_classes=["crypto-market-th", "change"]),
                Label(label="High", style_classes=["crypto-market-th", "high"]),
                Label(label="Low", style_classes=["crypto-market-th", "low"]),
            ],
        )

        self.rows_box = Box(
            name="crypto-market-rows",
            orientation="v",
            spacing=6,
        )

        self.content_card = Box(
            name="crypto-market-card",
            orientation="v",
            spacing=8,
            children=[self.table_header, self.rows_box],
        )

        self.children = [self.header, self.content_card]

    def _build_endpoint(self, query: str) -> str:
        configured = str(
            self._config.get(
                "endpoint",
                "https://api.coingecko.com/api/v3/simple/price",
            )
        ).strip()

        if "{query}" in configured:
            return configured.format(query=query)

        if "?" in configured:
            separator = "&" if not configured.endswith(("?", "&")) else ""
            return f"{configured}{separator}{query}"

        return f"{configured}?{query}"

    def _on_destroy(self, *_):
        if self._timer_id is not None:
            GLib.source_remove(self._timer_id)
            self._timer_id = None

    def _tick(self):
        self.refresh(force=True)
        return True

    def _format_price(self, value: float | None) -> str:
        if value is None:
            return "--"
        if value >= 1000:
            return f"{value:,.0f}"
        if value >= 1:
            return f"{value:.2f}"
        if value >= 0.01:
            return f"{value:.4f}"
        return f"{value:.6f}"

    def _format_change(self, value: float | None) -> str:
        if value is None:
            return "--"
        sign = "+" if value >= 0 else ""
        return f"{sign}{value:.2f}%"

    def _get_change_color(self, is_rising: bool) -> str:
        if self._red_rises:
            return "#ff704b" if is_rising else "#39c38c"
        return "#39c38c" if is_rising else "#ff704b"

    def _build_row(self, coin: str) -> Box:
        data = self._market_data.get(coin, {})

        close = data.get("close")
        high = data.get("high")
        low = data.get("low")
        change = data.get("change")
        is_rising = bool(data.get("is_rising", False))

        color = self._get_change_color(is_rising)

        coin_cell = Box(
            orientation="h",
            spacing=8,
            children=[
                Label(
                    label=self._COIN_ICONS.get(coin, "•"),
                    style_classes=["crypto-market-coin-icon", coin.lower()],
                ),
                Label(label=coin, style_classes=["crypto-market-coin-label"]),
            ],
        )

        price_label = Label(style_classes=["crypto-market-td", "price"])
        price_label.set_markup(
            f"<span foreground='{color}'>{self._format_price(close)}</span>"
        )

        change_label = Label(style_classes=["crypto-market-td", "change"])
        change_label.set_markup(
            f"<span foreground='{color}'>{self._format_change(change)}</span>"
        )

        high_label = Label(
            label=self._format_price(high),
            style_classes=["crypto-market-td", "high"],
        )

        low_label = Label(
            label=self._format_price(low),
            style_classes=["crypto-market-td", "low"],
        )

        return Box(
            name="crypto-market-row",
            orientation="h",
            spacing=10,
            children=[coin_cell, price_label, change_label, high_label, low_label],
        )

    def _render_rows(self):
        self._log(
            "[crypto_market] render rows=%s market_data_keys=%s",
            len(self._coins),
            list(self._market_data.keys()),
        )
        self.rows_box.children = [self._build_row(coin) for coin in self._coins]

    def _fetch_market_data(self) -> dict[str, dict]:
        coin_ids = [self._COIN_IDS[coin] for coin in self._coins]
        query = urlencode(
            {
                "ids": ",".join(coin_ids),
                "vs_currencies": "usd",
                "include_24hr_change": "true",
                "include_24hr_high_low": "true",
            }
        )

        endpoint = self._build_endpoint(query)
        self._log("[crypto_market] request endpoint=%s", endpoint)

        req = Request(endpoint, headers={"User-Agent": "tsumiki-crypto-market/1.0"})

        with urlopen(req, timeout=8) as response:
            status = getattr(response, "status", "?")
            payload = response.read().decode("utf-8", errors="replace")
        self._log(
            "[crypto_market] response status=%s payload_len=%s payload_head=%s",
            status,
            len(payload),
            payload[:220],
        )
        data = json.loads(payload)

        if not isinstance(data, dict):
            raise ValueError("Crypto API returned unexpected payload")
        if data.get("error"):
            raise ValueError(str(data.get("error")))

        parsed: dict[str, dict] = {}
        for coin in self._coins:
            coin_id = self._COIN_IDS[coin]
            item = data.get(coin_id, {})
            if not isinstance(item, dict):
                logger.warning(
                    "[crypto_market] coin missing coin=%s coin_id=%s item=%s",
                    coin,
                    coin_id,
                    item,
                )
                continue

            close = item.get("usd")
            change = item.get("usd_24h_change")
            high = item.get("usd_24h_high")
            low = item.get("usd_24h_low")

            if isinstance(close, (int, float)):
                parsed[coin] = {
                    "close": float(close),
                    "high": (
                        float(high) if isinstance(high, (int, float)) else float(close)
                    ),
                    "low": (
                        float(low) if isinstance(low, (int, float)) else float(close)
                    ),
                    "change": (
                        float(change) if isinstance(change, (int, float)) else 0.0
                    ),
                    "is_rising": (
                        float(change) >= 0
                        if isinstance(change, (int, float))
                        else True
                    ),
                }
            else:
                logger.warning(
                    (
                        "[crypto_market] close missing/invalid "
                        "coin=%s coin_id=%s close=%s item=%s"
                    ),
                    coin,
                    coin_id,
                    close,
                    item,
                )

        self._log(
            "[crypto_market] parsed coins=%s requested=%s",
            list(parsed.keys()),
            self._coins,
        )

        return parsed

    @run_in_thread
    def _refresh_async(self, generation: int):
        try:
            self._log("[crypto_market] refresh start generation=%s", generation)
            data = self._fetch_market_data()
            self._log(
                "[crypto_market] refresh success generation=%s coin_count=%s",
                generation,
                len(data),
            )
            idle_add(self._apply_refresh_result, generation, data)
        except Exception as err:
            logger.warning(f"[crypto_market] refresh failed: {err}")

    def _apply_refresh_result(self, generation: int, data: dict[str, dict]):
        if generation != self._request_generation:
            logger.warning(
                "[crypto_market] stale refresh generation=%s current=%s",
                generation,
                self._request_generation,
            )
            return False

        self._market_data = data
        self._log(
            "[crypto_market] apply refresh generation=%s keys=%s",
            generation,
            list(data.keys()),
        )
        self._render_rows()
        return False

    def refresh(self, force: bool = False):
        if not force and self._request_generation > 0:
            self._log(
                "[crypto_market] refresh skipped force=%s generation=%s",
                force,
                self._request_generation,
            )
            return
        self._request_generation += 1
        self._log(
            "[crypto_market] refresh queued force=%s generation=%s",
            force,
            self._request_generation,
        )
        self._refresh_async(self._request_generation)

    def _on_refresh_click(self, *_):
        print("Refresg")
        self.refresh(force=True)

    def close(self, *_):
        if self._parent is not None:
            self._parent.hide_popover()


class CryptoMarketWidget(ButtonWidget, PopoverMixin):
    """Bar widget for crypto market popup."""

    def __init__(self, **kwargs):
        super().__init__(name="crypto_market", **kwargs)

        self.container_box.children = nerd_font_icon(
            icon=self.config.get("icon", "󰠳"),
            props={"style_classes": ["panel-font-icon"]},
        )

        if self.config.get("label", False):
            self.container_box.add(
                Label(
                    label=self.config.get("label_text", "Crypto"),
                    style_classes=["panel-text"],
                )
            )

        if self.config.get("tooltip", True) and self.tooltips_enabled:
            self.set_tooltip_text(self.config.get("tooltip_text", "Crypto Market"))

        self.setup_popover(
            lambda: CryptoMarketPopoverContent(
                config={"widgets": {"crypto_market": self.config}},
                parent=self,
            ),
            connect_clicked=False,
        )
        self.connect("clicked", self._on_click)

    def _on_click(self, *_):
        popup = self.popup
        if popup and hasattr(popup, "content") and hasattr(popup.content, "refresh"):
            popup.content.refresh(force=False)
        self.toggle_popover()
