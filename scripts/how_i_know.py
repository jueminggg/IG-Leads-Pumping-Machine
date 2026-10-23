#!/usr/bin/env python3
"""Tag followers with how you know them, in quick batches.

    python3 scripts/how_i_know.py list [N]     # next N untagged (default 50)
    python3 scripts/how_i_know.py apply FILE   # read "handle = note" lines

List order: people you don't follow back first (Claude can't see their
posts if they're private, so your note matters most), newest followers first.
Notes: anything short, e.g. "poly classmate", "church", "ex-colleague",
"don't know" (Claude will deprioritise), "skip" (never contact).
"""
import sys
from pathlib import Path

from tracker import load, save


def untagged(rows):
    return [r for r in rows.values() if not r["how_i_know"]]


def main(args):
    rows = load()
    if not args or args[0] == "list":
        n = int(args[1]) if len(args) > 1 else 50
        todo = untagged(rows)
        # not-mutual first, then newest follow date first within each group
        todo.sort(key=lambda r: (r["mutual"] == "yes", -int((r["followed_since"] or "0000-00-00").replace("-", ""))))
        for r in todo[:n]:
            print(f"{r['handle']} = ")
        print(f"\n# {len(todo)} untagged left. Fill in after '=' and send back.", file=sys.stderr)
    elif args[0] == "apply":
        done = 0
        for line in Path(args[1]).read_text(encoding="utf-8").splitlines():
            if "=" not in line or line.lstrip().startswith("#"):
                continue
            handle, note = (x.strip() for x in line.split("=", 1))
            handle = handle.lstrip("@")
            if handle in rows and note:
                rows[handle]["how_i_know"] = note
                if note.lower() == "skip":
                    rows[handle]["status"] = "skip"
                done += 1
        save(rows)
        print(f"{done} tagged")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
