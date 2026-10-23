#!/usr/bin/env python3
"""List who needs a message today: replies waiting on you and follow-ups due.

Usage:
    python3 scripts/due.py            # as of today
    python3 scripts/due.py 2026-11-01 # as of a given date

Writes reports/_today.md and prints it.
"""
import sys
from datetime import date
from pathlib import Path

from tracker import load

TODAY_FILE = Path(__file__).resolve().parent.parent / "reports" / "_today.md"
DONE = {"client", "not_fit", "skip", "no_reply", "new"}


def main(as_of):
    rows = load().values()
    reply_now, due, upcoming = [], [], []
    for r in rows:
        if r["status"] in DONE:
            continue
        nf = r["next_followup"]
        if r["status"] == "replied":
            reply_now.append(r)
        elif nf and nf <= as_of:
            due.append(r)
        elif nf:
            upcoming.append(r)

    def line(r):
        late = f" (due {r['next_followup']})" if r["next_followup"] and r["next_followup"] < as_of else ""
        return f"- **@{r['handle']}** [{r['status']}]{late}: {r['next_step'] or 'see report'} -> reports/{r['handle']}.md"

    out = [f"# Follow-ups for {as_of}", ""]
    out += ["## Reply to these (they're waiting on you)"] + ([line(r) for r in reply_now] or ["- none"]) + [""]
    out += ["## Follow-ups due"] + ([line(r) for r in sorted(due, key=lambda r: r["next_followup"])] or ["- none"]) + [""]
    out += ["## Coming up"] + [f"- {r['next_followup']} @{r['handle']}: {r['next_step']}"
                               for r in sorted(upcoming, key=lambda r: r["next_followup"])[:10]] or ["- none"]
    text = "\n".join(out) + "\n"
    TODAY_FILE.parent.mkdir(exist_ok=True)
    TODAY_FILE.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat())
