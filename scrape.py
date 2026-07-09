"""
GST Council CGST Circulars -> RSS feed generator.

Scrapes https://gstcouncil.gov.in/cgst-circulars and writes docs/feed.xml
Run:  python scrape.py
"""

import sys
import datetime
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

SOURCE_URL = "https://gstcouncil.gov.in/cgst-circulars"
OUTPUT_FILE = "docs/feed.xml"
MAX_ITEMS = 20  # how many circulars to include in the feed

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; GSTCircularFeed/1.0; +https://github.com/)"
}


def fetch_page(url):
    """Download the page HTML."""
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse_circulars(html):
    """Pull each circular out of the table into a dictionary."""
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")
    if table is None:
        raise RuntimeError("No table found on the page - layout may have changed.")

    rows = table.find_all("tr")
    circulars = []

    for row in rows:
        cells = row.find_all("td")
        # Expect: Sr No | Circular No | Circular File | Date of issue | Subject
        if len(cells) < 5:
            continue  # skip the header row

        circular_no = cells[1].get_text(strip=True)

        # First PDF link in the "Circular File" cell
        link_tag = cells[2].find("a", href=True)
        pdf_link = link_tag["href"] if link_tag else SOURCE_URL
        if pdf_link.startswith("/"):
            pdf_link = "https://gstcouncil.gov.in" + pdf_link

        date_text = cells[3].get_text(strip=True)
        subject = cells[4].get_text(strip=True)

        # Parse DD-MM-YYYY into a real date; fall back to today if odd
        try:
            issued = datetime.datetime.strptime(date_text, "%d-%m-%Y")
        except ValueError:
            issued = datetime.datetime.utcnow()
        issued = issued.replace(tzinfo=datetime.timezone.utc)

        circulars.append(
            {
                "circular_no": circular_no,
                "pdf_link": pdf_link,
                "date": issued,
                "date_text": date_text,
                "subject": subject,
            }
        )

    if not circulars:
        raise RuntimeError("Table found but no circular rows parsed.")

    return circulars[:MAX_ITEMS]


def build_feed(circulars):
    """Turn the list of circulars into RSS XML."""
    fg = FeedGenerator()
    fg.id(SOURCE_URL)
    fg.title("CGST Circulars - GST Council")
    fg.link(href=SOURCE_URL, rel="alternate")
    fg.description(
        "Unofficial RSS feed of CGST Circulars published on the GST Council website."
    )
    fg.language("en")

    # Oldest first, so newest ends up at the top of the feed
    for c in reversed(circulars):
        entry = fg.add_entry()
        entry.id(c["pdf_link"])
        entry.title(f"Circular No. {c['circular_no']} - {c['subject'][:120]}")
        entry.link(href=c["pdf_link"])
        entry.pubDate(c["date"])
        entry.description(
            f"<p><b>Circular No:</b> {c['circular_no']}</p>"
            f"<p><b>Date of Issue:</b> {c['date_text']}</p>"
            f"<p><b>Subject:</b> {c['subject']}</p>"
            f'<p><a href="{c["pdf_link"]}">Download PDF</a></p>'
        )

    return fg


def main():
    print(f"Fetching {SOURCE_URL} ...")
    html = fetch_page(SOURCE_URL)

    print("Parsing circulars ...")
    circulars = parse_circulars(html)
    print(f"Found {len(circulars)} circulars. Newest: {circulars[0]['circular_no']}")

    print("Building feed ...")
    fg = build_feed(circulars)
    fg.rss_file(OUTPUT_FILE, pretty=True)
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
