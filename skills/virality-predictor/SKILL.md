---
name: virality-predictor
description: Predict the virality score (0-100) of a short-form video (TikTok, YouTube Shorts, Instagram Reels) and get per-platform editing advice, using the open-source AI Virality Predictor (OpenCV + Librosa features, scikit-learn model). Use when the user asks how viral a video will be, wants a virality score, or wants hook/pacing/audio feedback on a local video file (.mp4, .mov, .avi, .webm, .mkv).
---

# Virality Predictor

Wraps https://github.com/123angmish/ai-virality-predictor. The backend is run
locally; everything lives in `~/.virality-predictor` (override with the
`VIRALITY_HOME` environment variable).

## First use: install

Run once (needs `git` and Python 3.10+):

```bash
python3 "<this skill dir>/scripts/vp.py" install
```

On Windows use `python` instead of `python3`. This clones the repo and creates
a virtualenv with the backend's requirements.

## Analyse a video

```bash
python3 "<this skill dir>/scripts/vp.py" analyze "/path/to/video.mp4"
```

The script starts the local API on port 8765 if it is not running, uploads the
file to `/api/v1/analyze-upload` and prints the JSON result. Stop the server
afterwards with `python3 "<this skill dir>/scripts/vp.py" stop`.

## Presenting results

From the JSON, report to the user:
- `virality_score` (0-100)
- the 7 `features` in plain words: hook motion (first 3 s), scene cuts per
  minute, audio energy, speech tempo (WPM, ideal ~160-180), caption coverage,
  colour vibrancy, aspect ratio (0.5625 = 9:16 vertical)
- `platform_blueprints`: per-platform score and the editing tips
- 3 concrete edits that would most improve the weakest features

## Known limitations (tell the user when relevant)

- Upstream only really measures the VISUAL signals: `hook_motion_intensity`,
  `scene_cut_rate`, `color_vibrancy`, `resolution_aspect`, `duration_seconds`.
  `audio_rms_energy`, `transcript_wpm`, `text_overlay_ratio`,
  `transcript_snippet`, `video_summary`, face count and bass drop are hardcoded
  placeholders. Do NOT present them as analysis of the user's video; base advice
  only on the measured signals and say audio/speech/captions were not analysed.
- If feature extraction fails, the upstream backend silently substitutes fixed
  default features. If the features look exactly like
  hook 70.0 / cuts 18.0 / vibrancy 76.0 / duration 25.0, say the analysis failed and
  the score is not real.
- The upstream `analyze-url` endpoint ignores the URL and returns fixed values,
  so this skill only supports local files. For a link, download the video first.
- The score comes from a model trained on largely simulated data; present it as
  a rough heuristic, not a guarantee.
