import os, sys, subprocess, json, shutil

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

# --- Optional host-python dependency bootstrap (for cases where lib missing) ---
NEEDED_PKGS = [
    "fastmcp>=0.3.1",
    "requests",
    "pydantic>=2",
]

def _bootstrap_if_needed():
    try:
        import fastmcp  # type: ignore # noqa
        import pydantic  # noqa
    except Exception:  # broad: any import failure means we try
        pkgs = [p for p in NEEDED_PKGS]
        # Create per-extension user cache dir
        base_cache = os.path.join(os.path.expanduser("~"), ".cache", "naver_searchad_mcp")
        os.makedirs(base_cache, exist_ok=True)
        venv_dir = os.path.join(base_cache, "venv")
        if not os.path.exists(os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "python")):
            subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        python_bin = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "python")
        # Install packages if not already satisfied (simple heuristic by a marker file)
        marker = os.path.join(venv_dir, "installed.json")
        need_install = True
        if os.path.isfile(marker):
            try:
                with open(marker, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                if data.get("pkgs") == pkgs:
                    need_install = False
            except Exception:
                pass
        if need_install:
            subprocess.check_call([python_bin, "-m", "pip", "install", "--upgrade", "pip"])
            subprocess.check_call([python_bin, "-m", "pip", "install", *pkgs])
            with open(marker, "w", encoding="utf-8") as fh:
                json.dump({"pkgs": pkgs}, fh)
        # Prepend venv site-packages
        if venv_dir not in sys.prefix:
            site_dir = None
            if os.name == "nt":
                # Find site-packages under Lib
                cand = os.path.join(venv_dir, "Lib", "site-packages")
                if os.path.isdir(cand):
                    site_dir = cand
            else:
                for sub in ("lib",):
                    pyver = f"python{sys.version_info.major}.{sys.version_info.minor}"
                    cand = os.path.join(venv_dir, sub, pyver, "site-packages")
                    if os.path.isdir(cand):
                        site_dir = cand
                        break
            if site_dir and site_dir not in sys.path:
                sys.path.insert(0, site_dir)

_bootstrap_if_needed()

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
