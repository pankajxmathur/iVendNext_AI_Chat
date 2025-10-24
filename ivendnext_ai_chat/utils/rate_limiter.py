"""
Rate limiting utilities for AI Chat
"""

import frappe
from frappe import _
from datetime import datetime, timedelta
from typing import Optional


class RateLimiter:
    """Rate limiter for API requests"""

    CACHE_PREFIX = "ai_chat_rate_limit"

    def __init__(self):
        self.settings = frappe.get_cached_doc("AI Chat Settings")
        self.rate_limit = self.settings.rate_limit_per_user or 100

    def _get_cache_key(self, user: str) -> str:
        """Get cache key for user"""
        return f"{self.CACHE_PREFIX}:{user}"

    def _get_window_key(self) -> str:
        """Get current time window key (hourly)"""
        now = datetime.now()
        return now.strftime("%Y-%m-%d-%H")

    def check_limit(self, user: str) -> bool:
        """
        Check if user has exceeded rate limit

        Args:
            user: User email

        Returns:
            True if within limit

        Raises:
            Exception if rate limit exceeded
        """
        # System Managers bypass rate limiting
        if "System Manager" in frappe.get_roles(user):
            return True

        cache_key = self._get_cache_key(user)
        window_key = self._get_window_key()

        # Get current count from cache
        cache_data = frappe.cache().get_value(cache_key) or {}

        current_count = cache_data.get(window_key, 0)

        if current_count >= self.rate_limit:
            frappe.throw(
                _(f"Rate limit exceeded. Maximum {self.rate_limit} requests per hour allowed."),
                frappe.RateLimitExceededError,
            )

        return True

    def increment(self, user: str):
        """
        Increment request count for user

        Args:
            user: User email
        """
        # System Managers bypass rate limiting
        if "System Manager" in frappe.get_roles(user):
            return

        cache_key = self._get_cache_key(user)
        window_key = self._get_window_key()

        # Get current count
        cache_data = frappe.cache().get_value(cache_key) or {}

        # Clean old windows (keep only current and previous hour)
        now = datetime.now()
        prev_hour = (now - timedelta(hours=1)).strftime("%Y-%m-%d-%H")
        cache_data = {k: v for k, v in cache_data.items() if k in [window_key, prev_hour]}

        # Increment current window
        cache_data[window_key] = cache_data.get(window_key, 0) + 1

        # Save to cache (expire after 2 hours)
        frappe.cache().set_value(cache_key, cache_data, expires_in_sec=7200)

    def get_remaining(self, user: str) -> int:
        """
        Get remaining requests for user

        Args:
            user: User email

        Returns:
            Number of remaining requests
        """
        # System Managers have unlimited
        if "System Manager" in frappe.get_roles(user):
            return 999999

        cache_key = self._get_cache_key(user)
        window_key = self._get_window_key()

        cache_data = frappe.cache().get_value(cache_key) or {}
        current_count = cache_data.get(window_key, 0)

        return max(0, self.rate_limit - current_count)

    def reset(self, user: str):
        """
        Reset rate limit for user

        Args:
            user: User email
        """
        cache_key = self._get_cache_key(user)
        frappe.cache().delete_value(cache_key)


def check_rate_limit(user: Optional[str] = None):
    """
    Check and increment rate limit for user

    Args:
        user: User email (defaults to current user)

    Raises:
        Exception if rate limit exceeded
    """
    user = user or frappe.session.user
    limiter = RateLimiter()
    limiter.check_limit(user)
    limiter.increment(user)


def get_rate_limit_info(user: Optional[str] = None) -> dict:
    """
    Get rate limit information for user

    Args:
        user: User email (defaults to current user)

    Returns:
        Dict with limit info
    """
    user = user or frappe.session.user
    limiter = RateLimiter()

    return {
        "limit": limiter.rate_limit,
        "remaining": limiter.get_remaining(user),
        "window": "1 hour",
    }


@frappe.whitelist()
def reset_rate_limit(user: str):
    """
    Reset rate limit for user (System Manager only)

    Args:
        user: User email
    """
    if "System Manager" not in frappe.get_roles():
        frappe.throw(_("Only System Managers can reset rate limits"))

    limiter = RateLimiter()
    limiter.reset(user)

    return {"success": True, "message": f"Rate limit reset for {user}"}
