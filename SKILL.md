---
name: history-viewer
description: "Generate an HTML viewer for browsing past Claude Code conversation history. Extracts data from JSONL session files, builds a searchable/filterable UI. Invoke with /history."
user-invocable: true
argument-hint: "[--refresh]"
allowed-tools: "Bash, Read, Write"
---

# Claude Code History Viewer

Generates an HTML page + JSON data file to browse past Claude Code conversations in a browser.

## How it works

1. Run the Python extraction script to parse all JSONL session files
2. Output: `claude-history-data.json` (conversation data) + `claude-history-viewer.html` (UI)
3. Serve via `python3 -m http.server 8765` and open in browser

## Step 1: Generate data

Run the extraction script:

```bash
python3 ~/.claude/skills/history-viewer/extract.py
```

This reads all `~/.claude/projects/-Users-chethanbhatbs/*.jsonl` files and produces `~/claude-history-data.json`.

## Step 2: Ensure viewer HTML exists

The viewer HTML is at `~/claude-history-viewer.html`. If it doesn't exist, copy from the skill:

```bash
cp ~/.claude/skills/history-viewer/viewer.html ~/claude-history-viewer.html
```

## Step 3: Serve and open

```bash
cd ~ && python3 -m http.server 8765 &
open http://localhost:8765/claude-history-viewer.html
```

## Arguments

- `--refresh` — Force regenerate data even if `claude-history-data.json` already exists
- No args — Only regenerate if data file is missing or older than 1 hour

## Notes

- Data file can be large (4-5MB for ~40 sessions). Extraction takes 5-10 seconds.
- The viewer fetches `claude-history-data.json` via HTTP, so must be served (not opened as file://).
- Tool calls and tool results are excluded from the viewer to keep it readable. Only human text and Claude text responses are shown.
