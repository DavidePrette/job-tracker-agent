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


def fetch_html_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=USER_AGENT, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def looks_like_job_title(text: str) -> bool:
    if not text:
        return False
    text = text.strip()
    if len(text) < 8:
        return False

    lower = text.lower()
    if any(term in lower for term in NEGATIVE_TERMS):
        return False

    return any(term in lower for term in POSITIVE_TERMS)


def clean_href(base_url: str, href: str) -> str:
    return urljoin(base_url, href)