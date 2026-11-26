import base64
import json
import os
import pathlib
import sys

BUDGET = 140
ANCHOR = pathlib.Path(sys.argv[0] if sys.argv[0] else ".").resolve().parent
FEED = ANCHOR / "entry.txt"

raw = FEED.read_bytes()
line = raw.decode("utf-8").strip("\r\n")
tail = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
report = {
    "status": "accepted" if line.strip() and len(line) <= BUDGET else "rejected",
    "size": len(line),
    "budget": BUDGET,
    "dest": str(tail / "entry.txt"),
    "stamp": base64.b64encode(raw).decode("ascii")[:12],
}
if report["status"] != "accepted":
    print(json.dumps(report, ensure_ascii=False))
    sys.exit(1)
tail.mkdir(parents=True, exist_ok=True)
pathlib.Path(report["dest"]).write_bytes(raw)
report["done"] = True
print(json.dumps(report, ensure_ascii=False))
