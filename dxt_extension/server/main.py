import os, sys

# Robustly detect the extension root (directory that contains manifest.json or the package folder)
HERE = os.path.dirname(__file__)
candidate = HERE
EXT_ROOT = None
for _ in range(6):  # climb a few levels defensively
    if os.path.isfile(os.path.join(candidate, 'manifest.json')) or \
       os.path.isdir(os.path.join(candidate, 'naver_searchad_mcp')):
        EXT_ROOT = candidate
        break
    parent = os.path.dirname(candidate)
    if parent == candidate:
        break
    candidate = parent
if EXT_ROOT is None:
    # Fallback: one level up from server directory
    EXT_ROOT = os.path.abspath(os.path.join(HERE, '..'))

VENDOR_LIB = os.path.join(EXT_ROOT, 'server', 'lib')

for p in (EXT_ROOT, VENDOR_LIB):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

try:
    from naver_searchad_mcp.fastmcp_server import build_server, _apply_overrides  # type: ignore
except ModuleNotFoundError as e:
    print("[naver-searchad] Import error after path setup:", e, file=sys.stderr)
    print("[naver-searchad] Computed EXT_ROOT=", EXT_ROOT, file=sys.stderr)
    print("[naver-searchad] sys.path=\n" + "\n".join(sys.path), file=sys.stderr)
    raise

def main():  # pragma: no cover
    # Allow same CLI flags / env override logic
    _apply_overrides()
    server = build_server()
    server.run()

if __name__ == '__main__':
    main()
