"""
PCOIS2-26: Download/scrape Policy Database source documents.

Fetches the five policies scoped in Sprint 1 (PCOIS2-12) from the public
La Trobe Policy Library, saves the raw HTML (and the PDF version if the
page links to one), and writes a manifest recording the metadata fields
specified in PCOIS2-11: title, source URL, format, category, last
updated, access level.

NOTE ON VERIFICATION: I could not reach policies.latrobe.edu.au from my
sandbox to confirm the exact markup (search engines don't have it
indexed, and my environment's network is restricted to package
registries). The URL pattern below (document/view.php?id=N) is the one
Alina's Data Transformation doc already confirmed for policy 208. The
metadata-extraction patterns (version/status/review date) are written
against the general structure that platform uses (confirmed by fetching
RMIT's instance of the same underlying software, which La Trobe's site
mirrors closely) and against what Alina found by hand for policy 208.
Run this once on your own machine and spot-check data/raw/*.html against
the live pages - if any selector or regex misses, the comments below
mark where to adjust.

Output: data/raw/<id>.html [+ .pdf], data/manifest.json
"""
import json
import os
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

BASE = "https://policies.latrobe.edu.au/document/view.php"
OUT_DIR = "data/raw"
MANIFEST_PATH = "data/manifest.json"

# The five policies scoped in PCOIS2-12 (first five non-expired results
# from the Policy Library search, per datascopesprint1.docx).
POLICIES = [
    {"id": 208, "title": "Academic Dress Policy", "category": "Academic Affairs"},
    {"id": 220, "title": "Academic Progression Review Policy", "category": "Student Administration"},
    {"id": 76,  "title": "Academic Promotions Policy", "category": "Human Resources"},
    {"id": 420, "title": "Academic Staff Qualifications Policy", "category": "Human Resources"},
    {"id": 169, "title": "Admissions Policy", "category": "Student Administration"},
]

HEADERS = {"User-Agent": "PolicyDB-Chatbot-Capstone/1.0 (La Trobe CSE3CAP research project)"}


def fetch_policy(policy_id: int, session: requests.Session):
    url = f"{BASE}?id={policy_id}"
    resp = session.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return url, resp.text


def find_pdf_link(html: str, page_url: str):
    """Looks for a link to a PDF version of the policy. Adjust the label
    keywords here if La Trobe uses different wording than 'PDF'/'Print'."""
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        label = a.get_text(strip=True).lower()
        if href.lower().endswith(".pdf") or "pdf" in label or "print" in label:
            return requests.compat.urljoin(page_url, href)
    return None


def extract_metadata(html: str):
    """Best-effort extraction of version/status/review date from page text."""
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    version_match = re.search(r"Version\s+(\d+)", text, re.I)
    status = "current" if re.search(r"current version", text, re.I) else None
    review_match = re.search(r"Review Date[:\s]+([\d/]{6,10})", text, re.I)
    return {
        "version": version_match.group(1) if version_match else None,
        "status": status,
        "review_date": review_match.group(1) if review_match else None,
    }


def process_one(policy: dict, url: str, html: str) -> dict:
    """Shared by both the live fetch path and the offline test path."""
    os.makedirs(OUT_DIR, exist_ok=True)
    raw_path = os.path.join(OUT_DIR, f"{policy['id']}.html")
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(html)

    meta = extract_metadata(html)
    return {
        "id": policy["id"],
        "title": policy["title"],
        "category": policy["category"],
        "source_url": url,
        "document_format": "HTML",
        "access_level": "public",
        "version": meta["version"],
        "status": meta["status"],
        "review_date": meta["review_date"],
        "raw_html_path": raw_path,
        "raw_pdf_path": None,
    }


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    manifest = []
    with requests.Session() as session:
        for p in POLICIES:
            print(f"Fetching ({p['id']}) {p['title']} ...")
            try:
                url, html = fetch_policy(p["id"], session)
            except requests.RequestException as e:
                print(f"  FAILED: {e}", file=sys.stderr)
                continue

            entry = process_one(p, url, html)

            pdf_url = find_pdf_link(html, url)
            if pdf_url:
                try:
                    pdf_resp = session.get(pdf_url, headers=HEADERS, timeout=30)
                    pdf_resp.raise_for_status()
                    pdf_path = os.path.join(OUT_DIR, f"{p['id']}.pdf")
                    with open(pdf_path, "wb") as f:
                        f.write(pdf_resp.content)
                    entry["raw_pdf_path"] = pdf_path
                    entry["document_format"] = "HTML+PDF"
                except requests.RequestException as e:
                    print(f"  PDF fetch failed ({pdf_url}): {e}", file=sys.stderr)

            manifest.append(entry)
            time.sleep(1)  # be polite to the server

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nDone. {len(manifest)}/{len(POLICIES)} policies saved. Manifest: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
