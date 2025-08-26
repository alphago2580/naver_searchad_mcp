# bundled copy
from __future__ import annotations
import time, hmac, hashlib, base64, requests
from typing import List, Dict
BASE_URL = "https://api.searchad.naver.com"
BID_URI = "/estimate/average-position-bid/keyword"

def _sign(ts: str, method: str, uri: str, secret: str) -> bytes:
    return base64.b64encode(hmac.new(secret.encode('utf-8'), f"{ts}.{method}.{uri}".encode('utf-8'), hashlib.sha256).digest())

def build_headers(method: str, uri: str, keys: Dict[str,str]) -> Dict[str,str]:
    ts = str(int(time.time()*1000))
    return {
        'X-Timestamp': ts,
        'X-API-KEY': keys['API_KEY'],
        'X-Customer': str(keys['CUSTOMER_ID']),
        'X-Signature': _sign(ts, method, uri, keys['SECRET_KEY']),
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8'
    }

def estimate_bids(keywords: List[str], positions: List[int], devices: List[str], keys: Dict[str,str], timeout: int = 20) -> list[dict]:
    rows = []
    for device in devices:
        payload = {
            'device': device.upper(),
            'items': [{ 'key': kw, 'position': int(pos)} for kw in keywords for pos in positions]
        }
        hdr = build_headers('POST', BID_URI, keys)
        r = requests.post(BASE_URL + BID_URI, json=payload, headers=hdr, timeout=timeout)
        if r.status_code != 200:
            raise RuntimeError(f"Bid estimate failed device={device} status={r.status_code} body={r.text[:200]}")
        data = r.json()
        for row in data.get('estimate', []):
            row['device'] = device.upper()
            rows.append(row)
        time.sleep(0.25)
    return rows
