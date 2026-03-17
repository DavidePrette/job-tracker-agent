from datetime import datetime, timezone

import requests

from .base import BaseScraper


class NTNUScraper(BaseScraper):
    FEED_URL = (
        "https://www.ntnu.edu/vacancies?"
        "p_p_id=vacanciesportlet_WAR_vacanciesportlet&"
        "p_p_lifecycle=2&"
        "p_p_state=normal&"
        "p_p_mode=view&"
        "p_p_resource_id=feed&"
        "p_p_cacheability=cacheLevelPage"
    )

    def fetch_jobs(self) -> list[dict]:
        organization = self.source["organization"]
        default_city = self.source.get("city", "")

        response = requests.get(self.FEED_URL, timeout=40)
        response.raise_for_status()

        items = response.json()
        jobs = []
        seen = set()

        for item in items:
            href = str(item.get("url", "")).strip()
            if not href or href in seen:
                continue
            seen.add(href)

            title = " ".join(str(item.get("title", "")).split())
            if not title:
                continue

            city = " ".join(str(item.get("location", default_city)).split())
            deadline = item.get("deadline")
            posted_date = ""
            if isinstance(deadline, (int, float)):
                posted_date = datetime.fromtimestamp(
                    deadline / 1000, tz=timezone.utc
                ).strftime("%Y-%m-%d")

            summary = " ".join(
                [
                    title,
                    " ".join(str(item.get("description", "")).split()),
                    " ".join(str(item.get("type", "")).split()),
                ]
            ).strip()

            jobs.append(
                {
                    "organization": organization,
                    "title": title,
                    "location": city,
                    "posted_date": posted_date,
                    "url": href,
                    "summary": summary,
                }
            )

        return jobs