"""Credential loading utilities."""
from __future__ import annotations
import os
from typing import Dict

API_KEYS_FILE = "api_keys.txt"

class CredentialError(RuntimeError):
    pass

def load_api_keys(explicit: dict | None = None, search_paths: list[str] | None = None, allow_env: bool = True) -> Dict[str,str]:
    if explicit and len(explicit) == 3:
        return explicit
    env = {}
    if allow_env:
        env = {
            "API_KEY": os.getenv("NAVER_API_KEY"),
            "SECRET_KEY": os.getenv("NAVER_SECRET_KEY"),
            "CUSTOMER_ID": os.getenv("NAVER_CUSTOMER_ID"),
        }
        if all(env.values()):
            return env
    paths = search_paths or []
    keys = {}
    for base in paths:
        candidate = os.path.join(base, API_KEYS_FILE)
        if os.path.exists(candidate):
            with open(candidate, 'r', encoding='utf-8') as f:
                for line in f:
                    if ':' in line:
                        k,v=line.strip().split(': ',1); keys[k]=v
            break
    for k,v in env.items():
        if v and k not in keys:
            keys[k]=v
    missing = [k for k in ("API_KEY","SECRET_KEY","CUSTOMER_ID") if k not in keys]
    if missing:
        raise CredentialError(f"Missing credentials: {missing}")
    return keys
