# bot_user/services/shortener_service.py
"""
Async Shortener Service for Bot B (User Bot).

Reads shortener platform entries from MongoDB (settings.key == "shorteners"),
selects a platform (random), and attempts to shorten a redirect URL via the
shortener's API.

Admin-side shortener entries (as saved by admin) are expected to look like:
{
  "key": "shorteners",
  "value": [
    {"domain": "get2short.com", "api_key": "APIKEY123"},
    {"domain": "earn2short.com", "api_key": "APIKEY_ABC"}
  ]
}

Behavior:
 - If no shorteners configured → returns original redirect_url
 - Attempts an HTTP call to a shortener endpoint (GET) with a commonly used
   query format: https://{domain}/api?api={api_key}&url={redirect_url}
 - If the response JSON contains a url-like field (common keys: "short", "url",
   "short_url", "shortened"), it returns that value.
 - If the call fails (network error, timeout, unexpected response), returns
   the original redirect_url as a safe fallback.

This module uses aiohttp and is non-blocking so it can be called from async handlers.
"""

from typing import Optional, Dict, List
import random
import logging
import aiohttp
import asyncio
from urllib.parse import quote_plus

from core.database import db

logger = logging.getLogger(__name__)


class UserShortenerService:
    KEY = "shorteners"

    # Default HTTP settings
    DEFAULT_TIMEOUT = 8  # seconds
    RETRY_COUNT = 2

    @staticmethod
    def get_shorteners() -> List[Dict]:
        """
        Read configured shortener platforms from DB.
        Returns a list of dicts like: [{"domain": "get2short.com", "api_key": "ABC"}, ...]
        """
        doc = db.settings.find_one({"key": UserShortenerService.KEY})
        return doc["value"] if doc and "value" in doc else []

    @staticmethod
    def get_random_shortener() -> Optional[Dict]:
        """
        Pick a random shortener platform or return None if none configured.
        """
        items = UserShortenerService.get_shorteners()
        if not items:
            return None
        return random.choice(items)

    @staticmethod
    async def shorten_url(redirect_url: str, preferred: Optional[Dict] = None) -> str:
        """
        Attempt to shorten `redirect_url` using a shortener platform.

        Args:
            redirect_url: The long URL to shorten (usually your redirect server URL).
            preferred: Optional platform dict (overrides random selection).

        Returns:
            A shortened URL (string). On failure returns the original `redirect_url`.
        """
        shortener = preferred or UserShortenerService.get_random_shortener()
        if not shortener:
            # No shortener configured — fallback to original URL
            return redirect_url

        domain = shortener.get("domain")
        api_key = shortener.get("api_key", "")

        # Build a common API call. Many shorteners (including the ones used by
        # similar systems) accept a GET like:
        #  https://{domain}/api?api={api_key}&url={redirect_url}
        # We will try this pattern and parse the response.
        encoded = quote_plus(redirect_url)
        candidate_urls = [
            f"https://{domain}/api?api={api_key}&url={encoded}",
            f"https://{domain}/create?api={api_key}&url={encoded}",
            f"https://{domain}/shorten?api={api_key}&url={encoded}",
            # fallback attempt: some shorteners accept direct forwarding
            f"https://{domain}/?api={api_key}&url={encoded}",
        ]

        # Try a few candidate endpoints (some platforms use different paths)
        for url in candidate_urls:
            short = await UserShortenerService._try_shorten(url)
            if short:
                return short

        # Nothing worked — return original redirect_url
        logger.warning("ShortenerService: all attempts failed for domain=%s", domain)
        return redirect_url

    @staticmethod
    async def _try_shorten(api_call_url: str) -> Optional[str]:
        """
        Perform the HTTP GET request to the shortener API and attempt to extract
        a shortened URL from the response.

        Returns the shortened URL on success, otherwise None.
        """
        timeout = aiohttp.ClientTimeout(total=UserShortenerService.DEFAULT_TIMEOUT)

        for attempt in range(UserShortenerService.RETRY_COUNT + 1):
            try:
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(api_call_url, headers={"User-Agent": "TelegramFileBot/1.0"}) as resp:
                        text = await resp.text()

                        # Try JSON first
                        content_type = resp.headers.get("Content-Type", "")
                        if "application/json" in content_type:
                            try:
                                data = await resp.json()
                                # Common keys where shortened URL might be found
                                for key in ("short", "short_url", "url", "result", "data", "shortened"):
                                    if key in data:
                                        candidate = data[key]
                                        # If nested objects
                                        if isinstance(candidate, dict):
                                            # try to find nested 'url' or 'short'
                                            for k in ("url", "short", "short_url"):
                                                if k in candidate:
                                                    return candidate[k]
                                        elif isinstance(candidate, str) and candidate.startswith("http"):
                                            return candidate

                                # Some APIs return {'status':'ok','result':'https://...'}
                                if "result" in data and isinstance(data["result"], str) and data["result"].startswith("http"):
                                    return data["result"]

                            except Exception:
                                # JSON parsing failed — fall back to text parsing
                                pass

                        # If not JSON, try to extract URL from plain text (common for many shorteners)
                        # Quick heuristic: find http(s) substring
                        # This is a simple approach — not a full HTML parser (keeps dependency light)
                        idx = text.find("http")
                        if idx != -1:
                            # find end of URL (space or newline)
                            end = len(text)
                            for sep in (" ", "\n", "\r", '"', "'"):
                                pos = text.find(sep, idx)
                                if pos != -1:
                                    end = min(end, pos)
                            candidate = text[idx:end].strip()
                            if candidate.startswith("http"):
                                return candidate

            except asyncio.TimeoutError:
                logger.warning("ShortenerService: timeout for %s (attempt %d)", api_call_url, attempt + 1)
            except aiohttp.ClientError as e:
                logger.warning("ShortenerService: network error for %s: %s (attempt %d)", api_call_url, e, attempt + 1)
            except Exception as e:
                logger.exception("ShortenerService: unexpected error for %s: %s", api_call_url, e)

            # small backoff between retries
            await asyncio.sleep(0.4 * (attempt + 1))

        return None
