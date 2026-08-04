"""
PCOIS2-27: Build data cleaning & chunking script.

Implements the cleaning steps and chunking strategy Alina specified and
demonstrated by hand in Sprint 1 (PCOIS2-13/14), applied in code across
all five policies scraped by PCOIS2-26.

Cleaning steps (from PolicyDB Chatbot - Data Transformation, Alina):
  - Remove repeated "Top of Page" labels
  - Exclude website navigation / header / footer content
  - Remove excessive blank lines and spacing
  - Add a space after numbered clause markers: "(1)This" -> "(1) This"
  - Preserve section/part headings
  - Keep numbered clauses and list items as separate blocks
  - Convert tables into readable "decision -> responsible role" text
    (generalised here to "<column A header>: ... / <column B header>: ...")
  - Record policy title, version, status, review date and source URL

Chunking strategy (from the same document):
  - Chunk by existing section headings / numbered clauses, not fixed length
  - Keep related clauses together; only split at paragraph boundaries
  - Never split mid-sentence or mid-table-row
  - Never combine content from different policies
  - Attach policy title, section, and source URL to every chunk

Input:  data/raw/<id>.html + data/manifest.json      (from PCOIS2-26)
Output: data/cleaned/<id>.jsonl, data/cleaned/all_chunks.jsonl
"""
import json
import os
import re
from bs4 import BeautifulSoup, NavigableString, Tag

RAW_DIR = "data/raw"
MANIFEST_PATH = "data/manifest.json"
CLEANED_DIR = "data/cleaned"

MAX_CHUNK_CHARS = 1500  # soft cap; long sections split further at paragraph breaks
HEADING_RE = re.compile(r"^(Section|Part)\s+\d+\b", re.I)
CLAUSE_SPACING_RE = re.compile(r"\((\d+)\)(?=\S)")
NAV_LIKE_CLASSES = re.compile(r"nav|footer|header|breadcrumb|menu|skip-link", re.I)


def strip_boilerplate(soup: BeautifulSoup) -> Tag:
    """Remove nav/header/footer/breadcrumb elements and the repeated
    'Top of Page' links, then return the main content container."""
    for tag in soup.find_all(["nav", "header", "footer", "script", "style"]):
        tag.decompose()
    for tag in soup.find_all(class_=NAV_LIKE_CLASSES):
        tag.decompose()
    for a in soup.find_all("a"):
        if a.get_text(strip=True).lower() == "top of page":
            a.decompose()

    content = soup.find(id="content") or soup.find(attrs={"class": "content"}) or soup.body or soup
    return content


def table_to_text(table: Tag) -> str:
    """Convert a table into readable 'header: cell' text blocks instead of
    losing row/column structure, per Alina's before/after example."""
    rows = table.find_all("tr")
    if not rows:
        return ""
    headers = [th.get_text(strip=True) for th in rows[0].find_all(["th", "td"])]
    out_blocks = []
    body_rows = rows[1:] if rows[0].find_all("th") else rows
    for row in body_rows:
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if not cells:
            continue
        lines = []
        for i, cell in enumerate(cells):
            label = headers[i] if i < len(headers) and headers[i] else f"Column {i + 1}"
            lines.append(f"{label}: {cell}")
        out_blocks.append("\n".join(lines))
    return "\n\n".join(out_blocks)


def normalise_text(text: str) -> str:
    text = CLAUSE_SPACING_RE.sub(r"(\1) ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_sections(content: Tag):
    """Walk the content in document order, grouping blocks under the
    nearest preceding Section/Part heading. Returns a list of
    {heading, blocks: [text...]} preserving original order."""
    sections = []
    current = {"heading": "Preamble", "blocks": []}

    for el in content.descendants:
        if not isinstance(el, Tag):
            continue
        if el.name in ("h1", "h2", "h3", "h4"):
            heading_text = el.get_text(" ", strip=True)
            if HEADING_RE.match(heading_text) or el.name in ("h1", "h2"):
                if current["blocks"]:
                    sections.append(current)
                current = {"heading": heading_text, "blocks": []}
        elif el.name == "table":
            txt = table_to_text(el)
            if txt:
                current["blocks"].append(("table", txt))
        elif el.name in ("p", "li"):
            # skip if this element's text is purely inside a table we already handled
            if el.find_parent("table") is not None:
                continue
            txt = el.get_text(" ", strip=True)
            if txt and "doc-meta" not in (el.get("class") or []):
                current["blocks"].append(("para", txt))

    if current["blocks"]:
        sections.append(current)
    return sections


def split_long_section(heading: str, blocks):
    """Never split mid-sentence or mid-table-row: split only at block
    (paragraph/table) boundaries once the accumulated text passes the
    soft character cap."""
    chunks = []
    buf, buf_len = [], 0
    for kind, text in blocks:
        if buf and buf_len + len(text) > MAX_CHUNK_CHARS:
            chunks.append("\n\n".join(buf))
            buf, buf_len = [], 0
        buf.append(text)
        buf_len += len(text)
    if buf:
        chunks.append("\n\n".join(buf))
    return chunks if chunks else [""]


def extract_doc_meta(soup: BeautifulSoup):
    text = soup.get_text(" ", strip=True)
    version_match = re.search(r"Version\s+(\d+)", text, re.I)
    status = "current" if re.search(r"current version", text, re.I) else None
    review_match = re.search(r"Review Date[:\s]+([\d/]{6,10})", text, re.I)
    return {
        "version": version_match.group(1) if version_match else None,
        "status": status,
        "review_date": review_match.group(1) if review_match else None,
    }


def clean_and_chunk_policy(policy_meta: dict, html: str):
    soup = BeautifulSoup(html, "html.parser")
    doc_meta = extract_doc_meta(soup)
    content = strip_boilerplate(soup)
    sections = extract_sections(content)

    chunks = []
    for idx, sec in enumerate(sections):
        sub_chunks = split_long_section(sec["heading"], sec["blocks"])
        for sub_idx, text in enumerate(sub_chunks):
            clean_text = normalise_text(text)
            if not clean_text:
                continue
            chunks.append({
                "chunk_id": f"{policy_meta['id']}-{idx}-{sub_idx}",
                "policy_id": policy_meta["id"],
                "policy_title": policy_meta["title"],
                "category": policy_meta.get("category"),
                "section": sec["heading"],
                "version": policy_meta.get("version") or doc_meta["version"],
                "status": policy_meta.get("status") or doc_meta["status"],
                "review_date": policy_meta.get("review_date") or doc_meta["review_date"],
                "source_url": policy_meta["source_url"],
                "text": clean_text,
            })
    return chunks


def main():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        manifest = json.load(f)

    os.makedirs(CLEANED_DIR, exist_ok=True)
    all_chunks = []

    for policy in manifest:
        raw_path = policy["raw_html_path"]
        if not os.path.exists(raw_path):
            print(f"Skipping ({policy['id']}): raw HTML not found at {raw_path}")
            continue
        with open(raw_path, encoding="utf-8") as f:
            html = f.read()

        chunks = clean_and_chunk_policy(policy, html)
        all_chunks.extend(chunks)

        out_path = os.path.join(CLEANED_DIR, f"{policy['id']}.jsonl")
        with open(out_path, "w", encoding="utf-8") as f:
            for c in chunks:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        print(f"({policy['id']}) {policy['title']}: {len(chunks)} chunks -> {out_path}")

    combined_path = os.path.join(CLEANED_DIR, "all_chunks.jsonl")
    with open(combined_path, "w", encoding="utf-8") as f:
        for c in all_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"\nTotal: {len(all_chunks)} chunks across {len(manifest)} policies -> {combined_path}")


if __name__ == "__main__":
    main()
