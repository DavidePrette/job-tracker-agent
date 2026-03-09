from .base import BaseScraper
from .common import fetch_html_soup, clean_href, looks_like_job_title, NEGATIVE_TERMS


class GenericHubScraper(BaseScraper):
    def fetch_jobs(self) -> list[dict]:
        """
        For hub pages: collect promising outgoing vacancy links.
        """
        url = self.source["url"]
        organization = self.source["organization"]
        city = self.source.get("city", "")

        soup = fetch_html_soup(url)
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