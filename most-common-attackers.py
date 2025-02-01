#!/usr/bin/env python3
"""
This script reads fail2ban log file and prints the most common attackers.
"""

import re
from collections import Counter
from datetime import datetime, timedelta

LOG_FILE = "/var/log/fail2ban.log"


def parse_attackers(log_file, days=0, hours=0):
    """
    Parse the fail2ban log file and return a Counter object with the number of
    attacks per IP address.
    """
    start_time = datetime.now() - timedelta(days=days, hours=hours)
    attackers = Counter()
    with open(log_file, "r") as f:
        for line in f:
            match = re.search(
                r"^(\d{4}-\d{2}-\d{2}).* Ban (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$",
                line,
            )
            if match:
                timestamp = datetime.strptime(match.group(1), "%Y-%m-%d")
                ip = match.group(2)
                if timestamp >= start_time:
                    attackers[ip] += 1
    return attackers


def main(days=None, hours=None, log_file=LOG_FILE, num_attackers=10):
    attackers = parse_attackers(log_file, days=days, hours=hours)
    for ip, count in attackers.most_common(num_attackers):
        print(f"{ip}: {count} bans")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)

    # Create a mutually exclusive group for days and hours
    duration_group = parser.add_mutually_exclusive_group(required=True)
    duration_group.add_argument(
        "--days",
        type=int,
        default=0,
        help="Number of days to look back in log file (Default: 0)",
    )
    duration_group.add_argument(
        "--hours",
        type=int,
        default=0,
        help="Number of hours to look back in log file (Default: 0)",
    )

    parser.add_argument(
        "-l",
        "--log-file",
        type=str,
        default=LOG_FILE,
        help=f"Path to fail2ban log file (Default: {LOG_FILE})",
    )
    parser.add_argument(
        "-n",
        "--num-attackers",
        type=int,
        default=10,
        help="Number of most common attackers to print (Default: 10)",
    )
    args = parser.parse_args()

    main(**vars(args))
