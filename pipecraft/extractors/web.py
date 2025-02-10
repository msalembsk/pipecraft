import json
import logging
import time
from string import Template
from typing import ClassVar, Dict, List, Optional, Union

import cloudscraper

from pipecraft.extractors.base import BaseExtractor
from pipecraft.logger.default import get_default_logger


class WebExtractor(BaseExtractor):
    _scraper_instance: ClassVar[Optional[cloudscraper.CloudScraper]] = None

    @classmethod
    def get_scraper(cls) -> cloudscraper.CloudScraper:
        if cls._scraper_instance is None:
            cls._scraper_instance = cloudscraper.create_scraper(
                browser={"browser": "chrome", "platform": "windows", "mobile": False}
            )
        return cls._scraper_instance

    def __init__(
        self,
        source_name: str,
        url_template: str,
        headers: Optional[Dict] = None,
        cookies: Union[Dict, str, None] = None,
        delay_between_requests: float = 1.0,
        max_retries: int = 3,
        logger = None,
        **kwargs,
    ):
        super().__init__(source_name)
        self.logger = logger or get_default_logger()
        self.url_template = Template(url_template)
        
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.delay = delay_between_requests
        self.max_retries = max_retries
        self._set_cookies(cookies)
        self.scraper = self.get_scraper()

    def _set_cookies(self, cookies):
        if isinstance(cookies, str) and cookies.endswith((".json", ".txt")):
            with open(cookies) as f:
                self.cookies = json.load(f)
        elif isinstance(cookies, dict):
            self.cookies = cookies
        else:
            self.cookies = None

    def extract(self, params: Dict) -> str:
        url = self.url_template.safe_substitute(**params)
        response = self.scraper.get(url, headers=self.headers, cookies=self.cookies)
        response.raise_for_status()
        return response.text

    def extract_batch(self, params_list: List[Dict]) -> List[str]:
        results = []
        for params in params_list:
            try:
                result = self.extract(params)
                results.append(result)
                time.sleep(self.delay)
            except Exception as e:
                self.logger.error(f"Failed to extract {params}: {str(e)}")
                if len(results) < self.max_retries:
                    time.sleep(self.delay * 2)
                    continue
        return results
