import os, sys

# Ensure project root (directory containing naver_searchad_mcp) is on path
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..'))  # dxt root
PKG = ROOT
if PKG not in sys.path:
    sys.path.insert(0, PKG)

try:
    from naver_searchad_mcp.fastmcp_server import build_server, _apply_overrides  # type: ignore
except ModuleNotFoundError:
    # Fallback: try site-packages (user installed package) - this allows running even if code not bundled
    pass
    from naver_searchad_mcp.fastmcp_server import build_server, _apply_overrides  # type: ignore

def main():
    _apply_overrides()
    server = build_server()
    server.run()

if __name__ == '__main__':
    main()
