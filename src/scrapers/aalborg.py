import requests
from bs4 import BeautifulSoup

from .base import BaseScraper


class AalborgScraper(BaseScraper):
    API_URL = "https://www.aaudxp-data.aau.dk/api/v1/vacancies"
    CITY_MAP = {
        "aal": "Aalborg",
        "cph": "Copenhagen",
        "esb": "Esbjerg",
        "other": "Other city",
    }

    def fetch_jobs(self) -> list[dict]:
        organization = self.source["organization"]
        default_city = self.source.get("city", "")

        response = requests.get(self.API_URL, timeout=40)
        response.raise_for_status()
        items = response.json()

        jobs = []
        seen = set()

        for item in items:
            if "vip" not in (item.get("types") or []):
                continue

            vacancy_id = str(item.get("id", "")).strip()
            title = " ".join(str(item.get("title", "")).split())
            if not vacancy_id or not title:
                continue

            href = (
                "https://www.vacancies.aau.dk/scientific-positions/show-vacancy/"
                f"vacancyId/{vacancy_id}"
            )
            if href in seen:
                continue
            seen.add(href)

            raw_deadline = str(item.get("deadline", "")).strip()
            posted_date = raw_deadline.split(" ")[0] if raw_deadline else ""

            city_codes = item.get("cities") or []
            city_names = [self.CITY_MAP.get(code, code) for code in city_codes if code]
            location = ", ".join(city_names) if city_names else default_city

            department = " ".join(str(item.get("department", "")).split())
            intro = BeautifulSoup(str(item.get("introduction", "")), "lxml").get_text(" ", strip=True)
            summary = " ".join(part for part in [title, department, intro] if part).strip()

            jobs.append(
                {
                    "organization": organization,
                    "title": title,
                    "location": location,
                    "posted_date": posted_date,
                    "url": href,
                    "summary": summary,
                }
            )

        return jobs