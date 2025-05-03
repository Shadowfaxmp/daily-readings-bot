import requests
from bs4 import BeautifulSoup

def fetch_daily_readings(url=None):
    """
    Scrape the USCCB daily Bible readings page and return readings separately.
    Returns a dict mapping section headers ('Reading 1', 'Reading 2', 'Gospel') to their text or None if missing.
    """
    if url is None:
        url = "https://bible.usccb.org/daily-bible-reading"
    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content, "html.parser")
    # Define the sections to extract
    sections = ["Reading 1", "Reading 2", "Gospel"]
    readings = {}

    lectionary = soup.find("div", class_="wr-block b-lectionary padding-top-s padding-bottom-xxs bg-white")
    if lectionary:
        h2 = lectionary.find("h2")
        readings['title'] = h2.get_text(strip=True) if h2 else None
    else:
        readings['title'] = None


    for sec in sections:
        # Locate the section header
        header_tag = soup.find(lambda tag: tag.name == "h3" and tag.get_text(strip=True) == sec)
        if not header_tag:
            readings[sec] = None
            continue

        # Try to find the associated content-body div
        content_div = None
        parent = header_tag.parent
        if parent:
            # Often content-body is the next sibling of header's container
            content_div = parent.find_next_sibling("div", class_="content-body")
        # Fallback: search globally after header_tag
        if not content_div:
            content_div = header_tag.find_next("div", class_="content-body")

        if not content_div:
            readings[sec] = None
            continue

        # Extract all paragraphs inside content-body
        paragraphs = content_div.find_all("p")
        texts = [p.get_text(separator="\n", strip=True) for p in paragraphs if p.get_text(strip=True)]
        readings[sec] = "\n\n".join(texts) if texts else None

    return readings