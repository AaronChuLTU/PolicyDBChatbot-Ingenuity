"""
Discover current (non-expired) policies in the La Trobe Policy Library.

Parses the Policy Library search results listing, which renders one row per
document as:

    (00208) Academic Dress Policy
    (00211) Access to Assessed Material Retained by the University Policy  (Expired)

Rows marked "(Expired)" are excluded. Everything else is written to
data/policy_index.json for scrape_policies.py to consume.

Filtering here rather than after downloading matters for three reasons:
superseded policy text is exactly what the chatbot must never cite, expired
documents would roughly double the corpus for no benefit, and we avoid
hitting the university's server for pages we would then discard.

Two ways to run it:

  1. From a saved page (recommended - no guessing at URLs):
       In your browser, run the Policy Library search with
       Document Type = Policy, make sure ALL results are shown (not
       paginated), then Ctrl+S the page as data/policy_search.html

       python discover_policies.py --file data/policy_search.html

  2. Directly from a URL, once you know it:
       python discover_policies.py --url "https://policies.latrobe.edu.au/..."

Output: data/policy_index.json  ->  [{id, title, url, status}, ...]
"""
import argparse
import json
import os
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

BASE = "https://policies.latrobe.edu.au"
VIEW = f"{BASE}/document/view.php"
OUT_PATH = "data/policy_index.json"

HEADERS = {
    "User-Agent": "PolicyDB-Chatbot-Capstone/1.0 (La Trobe CSE3CAP research project)"
}

ID_IN_HREF = re.compile(r"view\.php\?id=(\d+)")
# Titles render as "(00208) Academic Dress Policy" - capture both parts.
TITLE_PATTERN = re.compile(r"^\(?0*(\d+)\)?\s*(.+)$")

# Words that mark a document as not current. "Expired" is what the listing
# uses; the others appear on individual document pages and are included so
# the same check can be reused downstream.
NOT_CURRENT = re.compile(r"expired|superseded|rescinded|no longer current", re.I)


def row_text_for(link) -> str:
    """Text of the row containing this link.

    The (Expired) marker is a sibling of the link, not inside it, so we look
    at the enclosing row. Falls back through a few container types because
    the listing may use <tr>, <li> or <div> depending on the view.
    """
    container = (
        link.find_parent("tr")
        or link.find_parent("li")
        or link.find_parent("div")
        or link.parent
    )
    return container.get_text(" ", strip=True) if container else link.get_text(strip=True)


def parse_listing(html: str):
    """Return (current, expired) policy lists."""
    soup = BeautifulSoup(html, "html.parser")
    current, expired = {}, {}

    for link in soup.find_all("a", href=True):
        match = ID_IN_HREF.search(link["href"])
        if not match:
            continue

        pid = int(match.group(1))
        label = link.get_text(" ", strip=True)

        # Strip the leading zero-padded ID from the visible title.
        title_match = TITLE_PATTERN.match(label)
        title = title_match.group(2).strip() if title_match else label

        if not title:
            continue

        entry = {
            "id": pid,
            "title": title,
            "url": f"{VIEW}?id={pid}",
            "status": "current",
        }

        if NOT_CURRENT.search(row_text_for(link)):
            entry["status"] = "expired"
            expired[pid] = entry
        else:
            current[pid] = entry

    # A policy appearing in both (e.g. linked twice) is treated as expired -
    # safer to exclude something current than to include something superseded.
    for pid in expired:
        current.pop(pid, None)

    return (
        [current[k] for k in sorted(current)],
        [expired[k] for k in sorted(expired)],
    )


def load_html(args) -> str:
    if args.file:
        if not os.path.exists(args.file):
            sys.exit(f"File not found: {args.file}")
        with open(args.file, encoding="utf-8", errors="replace") as f:
            return f.read()

    print(f"Fetching {args.url} ...")
    time.sleep(1.0)  # be considerate to a live university server
    resp = requests.get(args.url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


def main():
    parser = argparse.ArgumentParser(
        description="Discover current La Trobe policies from the search listing"
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", help="path to a saved copy of the search results page")
    source.add_argument("--url", help="URL of the search results page")
    parser.add_argument("--include-expired", action="store_true",
                        help="also include expired policies (not recommended)")
    args = parser.parse_args()

    html = load_html(args)
    current, expired = parse_listing(html)

    if not current and not expired:
        sys.exit(
            "No policy links found. Check that the saved page is the search\n"
            "RESULTS page (containing view.php?id= links), not the search form."
        )

    policies = current + expired if args.include_expired else current

    os.makedirs("data", exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(policies, f, indent=2, ensure_ascii=False)

    print(f"\nCurrent policies:  {len(current)}")
    print(f"Expired (skipped): {len(expired)}")
    print(f"Wrote {OUT_PATH} with {len(policies)} entries")

    print("\nFirst few:")
    for p in policies[:5]:
        print(f"  [{p['id']:>5}] {p['title']}")

    if expired and not args.include_expired:
        print("\nExcluded, for the record:")
        for p in expired[:5]:
            print(f"  [{p['id']:>5}] {p['title']}")
        if len(expired) > 5:
            print(f"  ... and {len(expired) - 5} more")

    print("\nNext: python scrape_policies.py")


if __name__ == "__main__":
    main()
