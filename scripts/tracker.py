"""Shared lead tracker layout and helpers."""
import csv
from pathlib import Path

TRACKER = Path(__file__).resolve().parent.parent / "data" / "leads.csv"
COLUMNS = [
    "handle", "profile_url", "followed_since", "status", "age_signal",
    "life_stage", "recent_activity", "message_sent", "date_sent",
    "last_reply", "last_reply_date", "followups_sent", "angles_used",
    "next_step", "next_followup", "notes",
]


def load():
    if not TRACKER.exists():
        return {}
    with TRACKER.open(newline="", encoding="utf-8") as f:
        return {r["handle"]: {c: r.get(c, "") for c in COLUMNS} for r in csv.DictReader(f)}


def save(rows):
    TRACKER.parent.mkdir(exist_ok=True)
    with TRACKER.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows.values())
