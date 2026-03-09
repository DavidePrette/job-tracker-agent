from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

USER_AGENT = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}

NEGATIVE_TERMS = [
    "privacy",
    "cookie",
    "cookies",
    "accessibility",
    "sitemap",
    "contact",
    "about us",
    "about",
    "login",
    "log in",
    "sign in",
    "subscribe",
    "terms of use",
    "terms",
    "gdpr",
    "dpo",
]

POSITIVE_TERMS = [
    "postdoc",
    "doctoral",
    "phd",
    "research",
    "researcher",
    "scientist",
    "engineer",
    "analyst",
    "professor",
    "position",
    "vacancy",
    "vacancies",
    "job",
    "jobs",
    "career",
    "careers",
    "project",
    "fellow",
    "student",
    "assistant professor",
    "associate professor",
]


def fetch_html(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=USER_AGENT, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def looks_like_job_title(text: str) -> bool:
    if not text:
        return False

    text = text.strip()
    if len(text) < 8:
        return False

    text_lower = text.lower()

    # reject obvious junk
    if any(term in text_lower for term in NEGATIVE_TERMS):
        return False

    # require job-like words
    return any(term in text_lower for term in POSITIVE_TERMS)


def scrape_generic_jobs(organization: str, city: str, url: str) -> list[dict]:
    soup = fetch_html(url)

    jobs = []
    seen = set()

    for a in soup.find_all("a", href=True):
        title = a.get_text(" ", strip=True)
        href = urljoin(url, a["href"])

        if not looks_like_job_title(title):
            continue

        href_lower = href.lower()
        if any(term in href_lower for term in NEGATIVE_TERMS):
            continue

        if href in seen:
            continue
        seen.add(href)

        jobs.append({
            "organization": organization,
            "title": title,
            "location": city or "",
            "posted_date": "",
            "url": href,
            "summary": title,
        })

    return jobs