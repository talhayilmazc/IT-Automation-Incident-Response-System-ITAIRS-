"""Very small demo log parser for text log files."""

from datetime import datetime
from pathlib import Path


def parse_log_file(path: str):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    events = []
    with p.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            events.append({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "line": line[:500],
            })
    return events


if __name__ == "__main__":
    from pprint import pprint
    sample_path = "example.log"
    Path(sample_path).write_text("INFO test log line 1\nERROR test line 2\n")
    pprint(parse_log_file(sample_path))
