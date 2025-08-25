"""Module entrypoint so you can run:
    python -m naver_searchad_mcp --api-key ...
Delegates to fastmcp_server.main().
"""
from .fastmcp_server import main

if __name__ == "__main__":  # pragma: no cover
    main()
