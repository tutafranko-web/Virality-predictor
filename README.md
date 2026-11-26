# Virality-predictor

Claude Code skill that wraps [ai-virality-predictor](https://github.com/123angmish/ai-virality-predictor)
to score short-form videos (0-100) and suggest edits per platform.

## Install on your computer

Requires `git` and Python 3.10–3.12 (Python 3.13+ won't work with the upstream
scikit-learn version, unless `uv` is installed, in which case it fetches 3.12).

macOS / Linux:
```bash
git clone -b claude/eager-clarke-yhtl4n https://github.com/tutafranko-web/Virality-predictor.git
mkdir -p ~/.claude/skills
cp -r Virality-predictor/skills/virality-predictor ~/.claude/skills/
python3 ~/.claude/skills/virality-predictor/scripts/vp.py install
```

Windows (PowerShell):
```powershell
git clone -b claude/eager-clarke-yhtl4n https://github.com/tutafranko-web/Virality-predictor.git
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse Virality-predictor\skills\virality-predictor "$HOME\.claude\skills\"
py -3.12 "$HOME\.claude\skills\virality-predictor\scripts\vp.py" install
```

Then restart Claude Code and ask e.g. *"Koliko je viralan video C:\Videos\reel.mp4?"*
or run `/virality-predictor`.
