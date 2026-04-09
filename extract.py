#!/usr/bin/env python3
"""Extract Claude Code conversation history from JSONL session files into a single JSON for the viewer."""

import json
import os
import glob
import sys
from pathlib import Path

PROJECTS_DIR = os.path.expanduser("~/.claude/projects/-Users-chethanbhatbs")
OUTPUT_FILE = os.path.expanduser("~/claude-history-data.json")


def extract_text(content):
    """Extract readable text from message content (string or list of blocks)."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                btype = block.get("type", "")
                if btype == "text":
                    parts.append(block.get("text", ""))
                elif btype == "tool_use":
                    name = block.get("name", "unknown")
                    parts.append(f"[Tool: {name}]")
                elif btype == "tool_result":
                    # Skip tool results — they're noisy
                    continue
                elif btype == "thinking":
                    # Skip thinking blocks
                    continue
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts).strip()
    return ""


def process_session(filepath):
    """Process a single JSONL session file. Returns (session_info, messages)."""
    session_id = Path(filepath).stem
    messages = []
    first_user_text = ""
    first_ts = None
    last_ts = None
    cwd = ""

    with open(filepath, "r", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            etype = entry.get("type", "")
            if etype not in ("user", "assistant"):
                continue

            ts = entry.get("timestamp")
            if ts and isinstance(ts, str):
                try:
                    ts = int(ts)
                except (ValueError, TypeError):
                    ts = None

            msg = entry.get("message", {})
            role = msg.get("role", etype)
            content = msg.get("content", "")
            text = extract_text(content)

            # Skip empty messages, pure tool results, pure tool calls
            if not text or text.startswith("[Tool:") and "\n" not in text:
                # If it's ONLY a tool call with no other text, skip
                if not text or all(
                    line.startswith("[Tool:") for line in text.split("\n") if line.strip()
                ):
                    continue

            if not cwd and entry.get("cwd"):
                cwd = entry["cwd"]

            if role == "user" and not first_user_text:
                # Get first meaningful user text (not tool results)
                clean = text.replace("[Tool:", "").strip()
                if clean:
                    first_user_text = clean[:120]

            if ts:
                if first_ts is None:
                    first_ts = ts
                last_ts = ts

            messages.append({"r": role, "t": text, "ts": ts})

    if not messages:
        return None, []

    session_info = {
        "id": session_id,
        "fm": first_user_text or "(no preview)",
        "ft": first_ts,
        "lt": last_ts,
        "n": len(messages),
        "p": cwd or "~",
    }

    return session_info, messages


def main():
    jsonl_files = sorted(
        glob.glob(os.path.join(PROJECTS_DIR, "*.jsonl")),
        key=lambda f: os.path.getmtime(f),
        reverse=True,
    )

    if not jsonl_files:
        print("No JSONL files found in", PROJECTS_DIR)
        sys.exit(1)

    print(f"Found {len(jsonl_files)} session files")

    sessions = []
    messages_map = {}
    total_msgs = 0

    for fpath in jsonl_files:
        info, msgs = process_session(fpath)
        if info and msgs:
            sessions.append(info)
            messages_map[info["id"]] = msgs
            total_msgs += len(msgs)

    # Sort sessions by last timestamp (most recent first)
    sessions.sort(key=lambda s: s.get("lt") or 0, reverse=True)

    data = {"s": sessions, "m": messages_map}

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, separators=(",", ":"))

    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    user_msgs = sum(1 for sid in messages_map for m in messages_map[sid] if m["r"] == "user")
    asst_msgs = total_msgs - user_msgs

    print(f"Extracted {len(sessions)} sessions, {total_msgs} messages ({user_msgs} user + {asst_msgs} assistant)")
    print(f"Output: {OUTPUT_FILE} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
