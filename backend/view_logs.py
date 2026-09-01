"""
view_logs.py

Tiny CLI to inspect the logged queries - handy for sprint demos and
QA review of hallucination/edge cases.

Usage:
    python view_logs.py            # show last 20 logs
    python view_logs.py --limit 5  # show last 5 logs
"""

import argparse
from query_logger import get_logs


def main():
    parser = argparse.ArgumentParser(description="View recent Policy DB Chatbot query logs")
    parser.add_argument("--limit", type=int, default=20, help="Number of logs to show")
    args = parser.parse_args()

    logs = get_logs(limit=args.limit)
    if not logs:
        print("No logs found yet. Run a query through the API first.")
        return

    for entry in logs:
        print("=" * 80)
        print(f"[{entry.id}] {entry.timestamp_utc}")
        print(f"Q: {entry.question}")
        print(f"A: {entry.final_answer}")
        print(f"Retrieved chunks ({len(entry.retrieved_chunks)}):")
        for chunk in entry.retrieved_chunks:
            print(f"   - {chunk}")
        if entry.metadata:
            print(f"Metadata: {entry.metadata}")
    print("=" * 80)


if __name__ == "__main__":
    main()
