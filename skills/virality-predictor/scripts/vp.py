#!/usr/bin/env python3
"""Install and run the AI Virality Predictor backend locally (stdlib only)."""
import json, os, subprocess, sys, time, uuid, urllib.request, urllib.error
from pathlib import Path

REPO = "https://github.com/123angmish/ai-virality-predictor.git"
HOME = Path(os.environ.get("VIRALITY_HOME", Path.home() / ".virality-predictor"))
SRC, VENV = HOME / "ai-virality-predictor", HOME / "venv"
PORT = int(os.environ.get("VIRALITY_PORT", "8765"))
BASE = f"http://127.0.0.1:{PORT}"
PIDFILE = HOME / "server.pid"
WIN = os.name == "nt"
PY = VENV / ("Scripts/python.exe" if WIN else "bin/python")


def run(cmd, **kw):
    print("+", " ".join(map(str, cmd)), file=sys.stderr)
    subprocess.check_call([str(c) for c in cmd], **kw)


def make_venv():
    # Upstream pins scikit-learn<1.5 (to load its pickled model), which has no
    # wheels for Python 3.13+, so the venv must use Python 3.10-3.12.
    import shutil
    if (3, 10) <= sys.version_info[:2] <= (3, 12):
        return run([sys.executable, "-m", "venv", VENV])
    for v in ("3.12", "3.11", "3.10"):
        cand = ["py", f"-{v}"] if WIN and shutil.which("py") else [shutil.which(f"python{v}")]
        if cand[0]:
            try:
                return run(cand + ["-m", "venv", VENV])
            except Exception:
                pass
    if shutil.which("uv"):
        return run(["uv", "venv", "--seed", "--python", "3.12", VENV])
    sys.exit("Need Python 3.10-3.12 (or 'uv'). Install Python 3.12 and re-run install.")


def install():
    HOME.mkdir(parents=True, exist_ok=True)
    if (SRC / ".git").exists():
        run(["git", "-C", SRC, "pull", "--ff-only"])
    else:
        run(["git", "clone", "--depth", "1", REPO, SRC])
    if not PY.exists():
        make_venv()
    run([PY, "-m", "pip", "install", "--upgrade", "pip"])
    run([PY, "-m", "pip", "install", "-r", SRC / "backend" / "requirements.txt"])
    print(f"Installed in {HOME}")


def alive():
    try:
        urllib.request.urlopen(BASE + "/api/v1/model-status", timeout=3).read()
        return True
    except Exception:
        return False


def start():
    if alive():
        return
    if not PY.exists():
        sys.exit("Not installed. Run: vp.py install")
    log = open(HOME / "server.log", "ab")
    kw = {"creationflags": 0x08000000} if WIN else {"start_new_session": True}
    p = subprocess.Popen([str(PY), "-m", "uvicorn", "main:app", "--host", "127.0.0.1",
                          "--port", str(PORT)], cwd=SRC / "backend",
                         stdout=log, stderr=log, **kw)
    PIDFILE.write_text(str(p.pid))
    for _ in range(90):
        if alive():
            return
        if p.poll() is not None:
            break
        time.sleep(1)
    sys.exit(f"Server did not start; see {HOME / 'server.log'}")


def stop():
    if PIDFILE.exists():
        pid = int(PIDFILE.read_text())
        try:
            if WIN:
                subprocess.call(["taskkill", "/F", "/PID", str(pid)])
            else:
                os.kill(pid, 15)
        except Exception:
            pass
        PIDFILE.unlink()
    print("stopped")


def analyze(path):
    f = Path(path)
    if not f.is_file():
        sys.exit(f"No such file: {f}")
    start()
    b = uuid.uuid4().hex
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{f.name}\"\r\n"
            "Content-Type: application/octet-stream\r\n\r\n").encode() + f.read_bytes() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request(BASE + "/api/v1/analyze-upload", data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    try:
        out = json.load(urllib.request.urlopen(req, timeout=600))
    except urllib.error.HTTPError as e:
        sys.exit(f"API error {e.code}: {e.read().decode(errors='replace')}")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "install": install()
    elif cmd == "start": start(); print(f"running at {BASE}")
    elif cmd == "stop": stop()
    elif cmd == "analyze" and len(sys.argv) > 2: analyze(sys.argv[2])
    else: sys.exit("usage: vp.py install | start | stop | analyze <video>")
