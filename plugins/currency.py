"""Launcher slash command: /currency — convert between world currencies.

Rates are downloaded from Frankfurter (https://frankfurter.dev) — free,
keyless, backed by 84 central banks — into a **per-day cache file** and
conversions read from that file instead of hitting the API on every query.
The file is refreshed at most once per calendar day and falls back to the
last snapshot if the network is unavailable.

Examples:
    /currency 100 usd to eur
    /currency 50 gbp jpy
    /currency usd eur          # amount defaults to 1
    /currency 10 dollars euros # common names and symbols work too
"""

import json
import os
import threading
import time
from datetime import date
from typing import ClassVar

from utils.constants import FX_RATES_CACHE_FILE
from utils.functions import get_http_client
from utils.plugin_manager import LauncherPlugin, PluginResult, copy_to_clipboard

#: Returns all EUR-based rates as a list of {date, base, quote, rate} rows.
_FRANKFURTER_RATES_URL = "https://api.frankfurter.dev/v2/rates"

# Frankfurter occasionally drops the very first connection attempt after a
# cold start (timeouts), so transient failures are retried a couple of times
# before giving up. Client errors (4xx) are not retried — they never recover.
_RETRY_ATTEMPTS = 3
_RETRY_DELAY_SECONDS = 0.5

# A valid snapshot has many quotes (the API returns ~164). A payload with
# fewer than this many rates is treated as malformed so it never poisons the
# daily cache file.
_MIN_RATES_COUNT = 10

# Serializes cache read/refresh so concurrent worker threads don't download
# the daily file twice.
_RATES_LOCK = threading.Lock()

#: Common names/symbols → ISO 4217 codes, so "dollar", "$" and "euro" work.
_COMMON_CURRENCIES = {
    "$": "USD",
    "dollar": "USD",
    "dollars": "USD",
    "buck": "USD",
    "bucks": "USD",
    "€": "EUR",
    "euro": "EUR",
    "euros": "EUR",
    "£": "GBP",
    "pound": "GBP",
    "pounds": "GBP",
    "quid": "GBP",
    "¥": "JPY",
    "yen": "JPY",
    "yuan": "CNY",
    "renminbi": "CNY",
    "rmb": "CNY",
    "rupee": "INR",
    "rupees": "INR",
    "₽": "RUB",
    "ruble": "RUB",
    "rubles": "RUB",
    "franc": "CHF",
    "francs": "CHF",
    "won": "KRW",
    "real": "BRL",
    "reais": "BRL",
    "peso": "MXN",
    "pesos": "MXN",
    "lira": "TRY",
    "krone": "DKK",
    "krona": "SEK",
    "zloty": "PLN",
    "koruna": "CZK",
    "forint": "HUF",
    "rand": "ZAR",
    "baht": "THB",
    "ringgit": "MYR",
    "shekel": "ILS",
    "dirham": "AED",
    "riyal": "SAR",
    "hryvnia": "UAH",
}


def _today() -> str:
    """Return today's date as ISO 8601 (yyyy-mm-dd)."""
    return date.today().isoformat()


def normalize_rows(rows: list) -> tuple[str, dict[str, float]]:
    """Turn the API's row list into (date, {quote: rate})."""
    rates: dict[str, float] = {}
    latest_date = ""
    for row in rows:
        if not isinstance(row, dict) or "quote" not in row or "rate" not in row:
            continue
        rates[str(row["quote"])] = float(row["rate"])
        row_date = str(row.get("date", ""))
        if row_date > latest_date:
            latest_date = row_date
    # Rates are EUR-based; EUR is always 1:1 with itself.
    rates["EUR"] = 1.0
    return latest_date or _today(), rates


def _download_rates() -> tuple[str, dict[str, float]]:
    """Download the latest EUR-based rates; returns (date, {quote: rate})."""
    for attempt in range(_RETRY_ATTEMPTS):
        try:
            response = get_http_client().get(_FRANKFURTER_RATES_URL)
            response.raise_for_status()
            fx_date, rates = normalize_rows(response.json())
            # Guard against malformed/empty payloads: a nearly-empty table
            # would poison the daily cache, so treat it as a failed download
            # and let the stale-cache fallback take over.
            if len(rates) < _MIN_RATES_COUNT:
                raise ValueError(
                    f"Frankfurter returned only {len(rates)} currency rate(s)"
                )
            return fx_date, rates
        except Exception as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            is_client_error = status is not None and 400 <= status < 500
            if is_client_error or attempt >= _RETRY_ATTEMPTS - 1:
                raise
            time.sleep(_RETRY_DELAY_SECONDS)
    raise RuntimeError("unreachable")  # pragma: no cover - loop returns or raises


def _read_cache() -> dict | None:
    """Return the cached {date, fetched, rates} payload, or None."""
    try:
        with open(FX_RATES_CACHE_FILE, "r", encoding="utf-8") as file:
            payload = json.load(file)
    except (OSError, ValueError):
        return None
    if not isinstance(payload, dict) or not isinstance(payload.get("rates"), dict):
        return None
    return payload


def _write_cache(payload: dict) -> None:
    """Persist the daily rates snapshot (best-effort)."""
    try:
        os.makedirs(os.path.dirname(FX_RATES_CACHE_FILE) or ".", exist_ok=True)
        with open(FX_RATES_CACHE_FILE, "w", encoding="utf-8") as file:
            json.dump(payload, file)
    except OSError:
        pass  # caching is best-effort; conversions still work this session


def load_rates() -> dict:
    """Return the daily rates payload, downloading it at most once a day.

    The cache counts as fresh when it was fetched today; otherwise the file
    is re-downloaded. A failed download falls back to the last snapshot
    rather than failing the conversion.
    """
    with _RATES_LOCK:
        cached = _read_cache()
        if cached and cached.get("fetched") == _today():
            return cached
        try:
            fx_date, rates = _download_rates()
        except Exception:
            if cached:  # network hiccup — use the last snapshot
                return cached
            raise
        payload = {"date": fx_date, "fetched": _today(), "rates": rates}
        _write_cache(payload)
        return payload


def fetch_rate(from_code: str, to_code: str) -> tuple[float, str]:
    """Return the (rate, date) converting *from_code* to *to_code*.

    Reads the locally cached per-day rates file; the network is only touched
    when the daily snapshot is missing or stale.
    """
    if from_code == to_code:
        return 1.0, _today()
    payload = load_rates()
    rates = payload["rates"]
    if from_code not in rates or to_code not in rates:
        raise ValueError(f"Unknown currency codes '{from_code}' / '{to_code}'")
    # All rates are EUR-based: X -> Y = (EUR -> Y) / (EUR -> X).
    return rates[to_code] / rates[from_code], str(payload.get("date", ""))


def normalize_code(token: str) -> str:
    """Return the ISO 4217 code for *token*, mapping common names/symbols."""
    token = token.strip().casefold()
    if token in _COMMON_CURRENCIES:
        return _COMMON_CURRENCIES[token]
    return token.upper()


def parse_query(args: str) -> tuple[float, str, str] | None:
    """Parse ``<amount> <from> [to] <to>`` into (amount, from_code, to_code).

    Returns None for an empty query; raises ValueError with a user-facing
    message when the expression can't be parsed.
    """
    tokens = args.strip().split()
    if not tokens:
        return None
    tokens = [token for token in tokens if token.casefold() != "to"]

    if len(tokens) == 2:
        # Two tokens: either "from to" (amount defaults to 1) or a numeric
        # amount with a missing target currency.
        try:
            amount = float(tokens[0].replace(",", ""))
        except ValueError:
            amount, from_cur, to_cur = 1.0, tokens[0], tokens[1]
        else:
            raise ValueError(
                f"Missing target currency: /currency {tokens[0]} {tokens[1]} <to>"
            )
    elif len(tokens) == 3:
        try:
            amount = float(tokens[0].replace(",", ""))
        except ValueError:
            raise ValueError(f"'{tokens[0]}' is not a valid amount")
        from_cur, to_cur = tokens[1], tokens[2]
    else:
        raise ValueError(
            "Expected: /currency <amount> <from> <to>  e.g. /currency 100 usd to eur"
        )

    from_code = normalize_code(from_cur)
    to_code = normalize_code(to_cur)
    if from_code == to_code:
        raise ValueError(f"'{from_code}' and '{to_code}' are the same currency")
    if (
        not from_code.isalpha()
        or not to_code.isalpha()
        or len(from_code) != 3
        or len(to_code) != 3
    ):
        raise ValueError(f"Unknown currency codes '{from_cur}' / '{to_cur}'")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    return amount, from_code, to_code


def format_money(value: float) -> str:
    """Format a monetary value compactly (up to 6 decimals, no trailing zeros)."""
    return f"{value:,.6f}".rstrip("0").rstrip(".")


class CurrencyPlugin(LauncherPlugin):
    """Slash command: /currency — convert amounts between currencies."""

    name = "currency"
    description = "Convert between currencies (daily rates, cached locally)"
    icon = "💱"
    aliases: ClassVar[list[str]] = ["fx", "money", "exchange"]
    # The first query of the day downloads the rates file, so give the user a
    # moment to finish typing before that happens.
    debounce_ms = 400

    def handle(self, args: str) -> list[PluginResult]:
        parsed = parse_query(args)
        if parsed is None:
            return [
                PluginResult(
                    "Usage: /currency <amount> <from> <to>",
                    subtitle=("e.g. /currency 100 usd to eur  or  /currency usd eur"),
                    icon=self.icon,
                )
            ]
        amount, from_code, to_code = parsed
        try:
            rate, date = fetch_rate(from_code, to_code)
        except Exception as exc:
            return [
                PluginResult(
                    "Conversion failed",
                    subtitle=f"{exc}",
                    icon="network-error-symbolic",
                )
            ]
        converted = amount * rate
        date_text = f" · {date}" if date else ""
        return [
            PluginResult(
                f"{format_money(amount)} {from_code} = "
                f"{format_money(converted)} {to_code}",
                subtitle=(
                    f"Rate {format_money(rate)} {from_code}→{to_code}"
                    f"{date_text} · Press Enter to copy"
                ),
                icon=self.icon,
                data=f"{format_money(converted)} {to_code}",
            )
        ]

    def execute(self, result: PluginResult | None = None) -> bool:
        if result is not None and result.data:
            copy_to_clipboard(str(result.data))
        return False  # close the launcher after copying
