"""FastMCP server entrypoint for package installation.

Usage:
  python -m naver_searchad_mcp.fastmcp_server --api-key ...
  or installed script: naver-searchad-mcp --api-key ...

Environment vars alternative:
  NAVER_API_KEY, NAVER_SECRET_KEY, NAVER_CUSTOMER_ID
"""
import argparse, json, os, time
from pathlib import Path
from typing import Dict
from fastmcp import FastMCP

from .credentials import load_api_keys
from .keyword_api import fetch_keyword_stats
from .bids_api import estimate_bids

BATCH_MAX = 5
CACHE_TTL = 60
RATE_SLEEP_SEC = 0.15
ESTIMATE_DEVICE_SLEEP = 0.25

mcp = FastMCP(name="naver-searchad")

_CACHE: dict[str, dict] = {}

def _cache_key(prefix: str, *parts: str) -> str:
    return prefix + '::' + '|'.join(parts)

def _cache_get(k: str):
    ent = _CACHE.get(k)
    if not ent: return None
    if time.time() - ent['t'] > CACHE_TTL:
        _CACHE.pop(k, None); return None
    return ent['v']

def _cache_set(k: str, v):
    _CACHE[k] = {"t": time.time(), "v": v}

@mcp.tool(description="Fetch keyword stats (batching + optional cache)")
def get_keyword_stats(keywords: list[str], show_detail: bool = True, use_cache: bool = True) -> list[dict]:
    if not keywords:
        return []
    keys = load_api_keys(search_paths=[os.getcwd(), os.path.dirname(os.getcwd())])
    results: list[dict] = []
    for i in range(0, len(keywords), BATCH_MAX):
        batch = keywords[i:i+BATCH_MAX]
        ck = _cache_key('KW', str(show_detail), *batch)
        if use_cache:
            cached = _cache_get(ck)
            if cached is not None:
                results.extend(cached); continue
        data = fetch_keyword_stats(batch, keys, show_detail=show_detail)
        results.extend(data)
        if use_cache:
            _cache_set(ck, data)
        time.sleep(RATE_SLEEP_SEC)
    return results

@mcp.tool(description="Estimate average position bids")
def estimate_average_position_bids(keywords: list[str], positions: list[int], devices: list[str] | None = None) -> list[dict]:
    if not keywords or not positions:
        return []
    devices = devices or ["PC","MOBILE"]
    keys = load_api_keys(search_paths=[os.getcwd(), os.path.dirname(os.getcwd())])
    return estimate_bids(keywords, positions, devices, keys)

@mcp.tool(description="Health check: returns static ok message")
def health() -> dict:
    return {"status":"ok","batch_max": BATCH_MAX, "cache_ttl": CACHE_TTL}

def build_server() -> FastMCP:
    return mcp

def _parse_args():
    ap = argparse.ArgumentParser(description="Naver SearchAd FastMCP Server")
    ap.add_argument("--api-key")
    ap.add_argument("--secret-key")
    ap.add_argument("--customer-id")
    ap.add_argument("--config", help="JSON file with API_KEY/SECRET_KEY/CUSTOMER_ID")
    ap.add_argument("--no-env", action="store_true")
    return ap.parse_args()

_OVERRIDES: Dict[str,str] = {}

def _apply_overrides():
    args = _parse_args()
    # 1) .env 로드 (있으면) - 기존 env 보다 먼저 파일 내용을 환경에 반영 (python-dotenv 없으면 무시)
    env_path = Path('.') / '.env'
    if env_path.exists():
        try:
            from dotenv import dotenv_values
            dot_vals = dotenv_values(env_path)
            for k,v in dot_vals.items():
                if v is not None and k.startswith('NAVER_') and k not in os.environ:
                    os.environ[k] = v
        except Exception:
            pass
    cfg: Dict[str,str] = {}
    if args.config and os.path.exists(args.config):
        with open(args.config,'r',encoding='utf-8') as f:
            raw = json.load(f)
        for k in ("API_KEY","SECRET_KEY","CUSTOMER_ID"):
            if k in raw and raw[k]:
                cfg[k]=str(raw[k])
    if args.api_key: cfg['API_KEY']=args.api_key
    if args.secret_key: cfg['SECRET_KEY']=args.secret_key
    if args.customer_id: cfg['CUSTOMER_ID']=args.customer_id
    global _OVERRIDES
    if cfg:
        _OVERRIDES = cfg
        for k,v in cfg.items():
            if k == 'API_KEY': os.environ['NAVER_API_KEY']=v
            elif k == 'SECRET_KEY': os.environ['NAVER_SECRET_KEY']=v
            elif k == 'CUSTOMER_ID': os.environ['NAVER_CUSTOMER_ID']=v
    if args.no_env:
        for k in ('NAVER_API_KEY','NAVER_SECRET_KEY','NAVER_CUSTOMER_ID'):
            os.environ.pop(k, None)

def main():  # pragma: no cover
    _apply_overrides()
    mcp.run()

if __name__ == '__main__':  # pragma: no cover
    main()
