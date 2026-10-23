#!/usr/bin/env python3
"""Turn Instagram's "Download your information" followers export into a lead tracker.

Usage:
    python3 scripts/parse_followers.py followers_1.json [following.json ...]

Pass the followers file(s) and, optionally, your following file. Files whose
name contains "following" (or whose data is "relationships_following") are
used to mark each follower as mutual = yes/no (you follow them back).

Writes data/leads.csv. Existing rows are kept, so re-running after a new
export only adds new followers and never wipes your notes.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from tracker import COLUMNS, TRACKER, load, save


def iter_entries(data):
    """Yield (handle, url, timestamp) from any known export layout."""
    if isinstance(data, dict):
        # e.g. {"relationships_followers": [...]}
        for value in data.values():
            if isinstance(value, list):
                yield from iter_entries(value)
        return
    for item in data:
        for s in item.get("string_list_data", []):
            handle = s.get("value") or item.get("title")
            url = s.get("href", "")
            if not handle and url:
                handle = url.rstrip("/").split("/")[-1]
            if handle:
                yield handle, url or f"https://www.instagram.com/{handle}", s.get("timestamp")


def main(paths):
    rows = load()
    before = len(rows)

    following = set()
    for p in paths:
        data = json.loads(Path(p).read_text(encoding="utf-8"))
        if "following" in Path(p).name.lower() or (
                isinstance(data, dict) and "relationships_following" in data):
            following |= {h for h, _, _ in iter_entries(data)}
            continue
        for handle, url, ts in iter_entries(data):
            if handle in rows:
                continue
            since = datetime.fromtimestamp(ts, timezone.utc).date().isoformat() if ts else ""
            rows[handle] = {c: "" for c in COLUMNS} | {
                "handle": handle, "profile_url": url,
                "followed_since": since, "status": "new",
            }

    if following:
        for handle, r in rows.items():
            r["mutual"] = "yes" if handle in following else "no"

    save(rows)
    print(f"{len(rows) - before} new followers added, {len(rows)} total -> {TRACKER}")
    if following:
        n = sum(r["mutual"] == "yes" for r in rows.values())
        print(f"{n} mutual (you follow them back), {len(rows) - n} not")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
