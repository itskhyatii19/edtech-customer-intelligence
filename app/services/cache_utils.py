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


def get_cache_ttl_minutes(default: int = 60) -> int:
    return st.session_state.get(CACHE_KEY, default)


def set_cache_ttl_minutes(value: int):
    st.session_state[CACHE_KEY] = int(value)


def clear_all_cache():
    # Clear Streamlit's cache and bump the reset token so cached functions
    # using the cache-buster will be forced to recompute.
    st.cache_data.clear()
    st.session_state[RESET_KEY] = st.session_state.get(RESET_KEY, 0) + 1


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

    reset = st.session_state.get(RESET_KEY, 0)
    return f"{key}:{bucket}:{reset}"
