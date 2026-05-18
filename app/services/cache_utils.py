"""Cache utilities for Settings page.

Provides simple helpers to store a user-selected cache TTL in session state
and to clear Streamlit's cache. Note: `st.cache_data` decorators are applied
at import time; changing TTL here affects stored setting and workflows that
explicitly read this setting, but won't change decorator-bound TTL until
functions are refactored to use programmatic caching.
"""
import streamlit as st
import time


RESET_KEY = "cache_reset"

CACHE_KEY = "cache_ttl_minutes"

_FALLBACK_STATE: dict[str, int] = {}


def _get_state() -> dict:
    try:
        return st.session_state
    except Exception:
        return _FALLBACK_STATE


def get_cache_ttl_minutes(default: int = 60) -> int:
    state = _get_state()
    return int(state.get(CACHE_KEY, default))


def set_cache_ttl_minutes(value: int):
    state = _get_state()
    state[CACHE_KEY] = int(value)


def clear_all_cache():
    # Clear Streamlit's cache and bump the reset token so cached functions
    # using the cache-buster will be forced to recompute.
    try:
        st.cache_data.clear()
    except Exception:
        pass

    state = _get_state()
    state[RESET_KEY] = int(state.get(RESET_KEY, 0)) + 1


def make_cache_buster(key: str) -> str:
    """Create a cache buster token that changes when TTL windows expire

    The token is derived from the TTL (minutes) and current time so that
    cached functions that accept this token will be recomputed when the
    TTL window elapses or when `clear_all_cache()` increments the reset.
    """
    ttl = get_cache_ttl_minutes()
    if ttl <= 0:
        bucket = 0
    else:
        bucket = int(time.time() / (ttl * 60))

    state = _get_state()
    reset = int(state.get(RESET_KEY, 0))
    return f"{key}:{bucket}:{reset}"


def cache_buster_for_key(key: str) -> str:
    """Return the current cache buster token for a specific key."""
    return make_cache_buster(key)


def verify_cache_helpers(test_ttl: int = 7) -> dict:
    """Run lightweight cache helper verification without expensive pipelines."""
    original_ttl = get_cache_ttl_minutes()
    set_cache_ttl_minutes(test_ttl)
    token_before = make_cache_buster("verify_cache")
    clear_all_cache()
    token_after = make_cache_buster("verify_cache")
    set_cache_ttl_minutes(original_ttl)

    return {
        "pass": token_before != token_after,
        "original_ttl": original_ttl,
        "test_ttl": test_ttl,
        "token_before_clear": token_before,
        "token_after_clear": token_after,
        "current_ttl": get_cache_ttl_minutes(),
        "cache_cleared": token_before != token_after,
    }
