"""Simple diagnostics runner that can be scheduled or called manually."""

import platform
import psutil
from datetime import datetime


def run_diagnostics():
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "hostname": platform.node(),
        "os": f"{platform.system()} {platform.release()}",
        "cpu_percent": psutil.cpu_percent(interval=0.2),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
    }
    return report


if __name__ == "__main__":
    from pprint import pprint
    pprint(run_diagnostics())
