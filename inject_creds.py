"""
inject_creds.py — NexGen AI Portal credential injector
-------------------------------------------------------
Run by GitHub Actions on every push to main.
Reads passwords from environment variables (GitHub Secrets),
base64-encodes them (matching btoa() in the browser), and
replaces %%PLACEHOLDER%% strings in the HTML source files.

Output is written to ./dist/ — GitHub Actions deploys that folder
to the gh-pages branch. The main branch source never contains
real passwords.

Required GitHub Secrets:
  CRED_NEXGEN    — password for username "nexgen"
  CRED_TRAINER1  — password for username "trainer1"
  CRED_VAMSI     — password for username "vamsi"
  MASTER_CODE    — master access code (any username)
"""

import base64, json, os, pathlib, shutil, sys

# ── Helper ──────────────────────────────────────────────────────────────────
def b64(s: str) -> str:
    """Matches browser btoa(): UTF-8 string → base64."""
    return base64.b64encode(s.encode("utf-8")).decode("ascii")


# ── Read secrets from environment ───────────────────────────────────────────
def require(key: str) -> str:
    val = os.environ.get(key, "")
    if not val:
        print(f"WARNING: {key} is empty. Credential injection may be incomplete.", file=sys.stderr)
    return val

cred_nexgen   = require("CRED_NEXGEN")
cred_trainer1 = require("CRED_TRAINER1")
cred_vamsi    = require("CRED_VAMSI")
master_code   = require("MASTER_CODE")

# Build USERS dict: { btoa(username): btoa(password), ... }
users = {
    b64("nexgen"):   b64(cred_nexgen),
    b64("trainer1"): b64(cred_trainer1),
    b64("vamsi"):    b64(cred_vamsi),
}

# Encode the whole USERS JSON so the HTML just does: JSON.parse(atob('...'))
users_b64  = b64(json.dumps(users, separators=(",", ":")))
master_b64 = b64(master_code)

print(f"Credentials encoded. Users: {list(users.keys())}")
print(f"USERS_B64 length: {len(users_b64)} chars")


# ── Build dist/ ─────────────────────────────────────────────────────────────
dist = pathlib.Path("dist")
if dist.exists():
    shutil.rmtree(dist)

# Copy everything except things that shouldn't be deployed
shutil.copytree(
    ".",
    str(dist),
    ignore=shutil.ignore_patterns(
        ".git", ".github", "dist", "__pycache__", "*.py", "*.pyc",
    ),
)

print(f"Copied source tree to {dist}/")


# ── Inject into HTML files ───────────────────────────────────────────────────
def inject(path: pathlib.Path):
    if not path.exists():
        print(f"SKIP (not found): {path}")
        return
    text = path.read_text(encoding="utf-8")
    before = text.count("%%USERS_B64%%") + text.count("%%MASTER_B64%%")
    text = text.replace("%%USERS_B64%%", users_b64)
    text = text.replace("%%MASTER_B64%%", master_b64)
    path.write_text(text, encoding="utf-8")
    print(f"Injected {before} placeholder(s) in {path}")

inject(dist / "index.html")
inject(dist / "teacher-guide.html")

print("Done. Deploy ./dist to GitHub Pages.")
