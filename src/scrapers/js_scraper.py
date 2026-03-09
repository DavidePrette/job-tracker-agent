from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from .base import BaseScraper
from .common import clean_href, looks_like_job_title, NEGATIVE_TERMS


class GenericJSScraper(BaseScraper):
    def fetch_jobs(self) -> list[dict]:
        url = self.source["url"]
        organization = self.source["organization"]
        city = self.source.get("city", "")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(3000)

            for label in ["Accept", "Accept all", "Allow all cookies", "I agree", "OK"]:
                try:
                    page.get_by_text(label, exact=False).click(timeout=1500)
                    page.wait_for_timeout(1000)
                    break
                except Exception:
                    pass

            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "lxml")

        jobs = []
        seen = set()

        for a in soup.find_all("a", href=True):
            title = a.get_text(" ", strip=True)
            href = clean_href(url, a["href"])

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
                "location": city,
                "posted_date": "",
                "url": href,
                "summary": title,
            })

        return jobs