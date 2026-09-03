"""GitHub tray widget package.

The bar button and popover live in :mod:`widgets.github_tray.widget`;
``gh`` CLI access in :mod:`widgets.github_tray.client`, pure helpers in
:mod:`widgets.github_tray.state` and reusable components in
:mod:`widgets.github_tray.components`.
"""

from .client import GitHubClient, GitHubClientError
from .widget import GitHubTrayPopoverContent, GitHubTrayWidget

__all__ = [
    "GitHubClient",
    "GitHubClientError",
    "GitHubTrayPopoverContent",
    "GitHubTrayWidget",
]
