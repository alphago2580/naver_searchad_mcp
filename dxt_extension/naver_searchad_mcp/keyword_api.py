# bundled copy
from __future__ import annotations
import time, hmac, hashlib, base64, requests
from typing import List, Dict
BASE_URL = "https://api.searchad.naver.com"
KEYWORDS_URI = "/keywordstool"

def _sign(ts: str, method: str, uri: str, secret: str) -> bytes:
    return base64.b64encode(hmac.new(secret.encode('utf-8'), f"{ts}.{method}.{uri}".encode('utf-8'), hashlib.sha256).digest())

def build_headers(method: str, uri: str, keys: Dict[str,str]) -> Dict[str,str]:
    ts = str(int(time.time()*1000))
    return {
        'X-Timestamp': ts,
        'X-API-KEY': keys['API_KEY'],
        'X-Customer': str(keys['CUSTOMER_ID']),
        'X-Signature': _sign(ts, method, uri, keys['SECRET_KEY']),
        'Accept': 'application/json'
    }

def safe_int(x):
    try:
        if isinstance(x,str) and '<' in x: return 9
        return int(x)
    except Exception:
        return 0

def sum_search(pc, mobile):
    return safe_int(pc) + safe_int(mobile)

def fetch_keyword_stats(keywords: List[str], keys: Dict[str,str], show_detail: bool = True, timeout: int = 15) -> list[dict]:
    if not keywords:
        return []
    params = {"hintKeywords": ",".join(keywords), "showDetail": '1' if show_detail else '0'}
    hdr = build_headers('GET', KEYWORDS_URI, keys)
    r = requests.get(BASE_URL + KEYWORDS_URI, params=params, headers=hdr, timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError(f"Keyword API failed status={r.status_code} body={r.text[:200]}")
    items = r.json().get('keywordList', [])
    out = []
    for it in items:
        out.append({
            'keyword': it.get('relKeyword'),
            'monthlyPcSearch': it.get('monthlyPcQcCnt'),
            'monthlyMobileSearch': it.get('monthlyMobileQcCnt'),
            'monthlyAvgPcClick': it.get('monthlyAvePcClkCnt'),
            'monthlyAvgMobileClick': it.get('monthlyAveMobileClkCnt'),
            'competition': it.get('compiScore'),
            'monthlyTotalSearch': sum_search(it.get('monthlyPcQcCnt'), it.get('monthlyMobileQcCnt')),
        })
    return out
