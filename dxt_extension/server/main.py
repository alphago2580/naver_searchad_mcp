import os, sys

# Adjust path so we can import the installed package if running from source clone
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from naver_searchad_mcp.fastmcp_server import build_server, _apply_overrides  # type: ignore

def main():  # pragma: no cover
    # Allow same CLI flags / env override logic
    _apply_overrides()
    server = build_server()
    server.run()

if __name__ == '__main__':
    main()
