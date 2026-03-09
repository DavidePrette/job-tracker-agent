from abc import ABC, abstractmethod


class BaseScraper(ABC):
    def __init__(self, source: dict):
        self.source = source

    @abstractmethod
    def fetch_jobs(self) -> list[dict]:
        pass