import http.cookiejar
import json
from typing import Callable, Dict, Optional, Union

import requests

from .base import BaseExtractor


class APIExtractor(BaseExtractor):
    def __init__(
        self,
        source_name: str,
        base_url: str,
        method: str = "GET",
        headers: Optional[Dict] = None,
        cookies: Union[Dict, str, http.cookiejar.CookieJar, None] = None,
        auth_callback: Optional[Callable[[], str]] = None,
        payload: Optional[Dict] = None,
        params: Optional[Dict] = None,
        save_raw: bool = True,
        output_path: Optional[str] = None,
        verify_ssl: bool = True,
        proxy: Optional[Dict] = None,
    ):
        super().__init__(source_name, save_raw, output_path)
        self.base_url = base_url
        self.method = method.upper()
        self.headers = headers or {}
        self.payload = payload
        self.params = params
        self.verify_ssl = verify_ssl
        self.proxy = proxy
        self._set_cookies(cookies)
        self._set_auth(auth_callback)

    def _set_cookies(self, cookies):
        if isinstance(cookies, str) and cookies.endswith((".json", ".txt")):
            with open(cookies) as f:
                self.cookies = json.load(f)
        elif isinstance(cookies, dict):
            self.cookies = cookies
        elif isinstance(cookies, http.cookiejar.CookieJar):
            self.cookies = cookies
        else:
            self.cookies = None

    def _set_auth(self, auth_callback):
        if auth_callback:
            token = auth_callback()
            self.headers["Authorization"] = f"Bearer {token}"

    def extract(self) -> Dict:
        request_kwargs = {
            "url": self.base_url,
            "headers": self.headers,
            "cookies": self.cookies,
            "timeout": self.timeout,
            "verify": self.verify_ssl,
            "proxies": self.proxy,
        }

        if self.method in ["POST", "PUT", "PATCH"]:
            request_kwargs["json"] = self.payload
        elif self.params:
            request_kwargs["params"] = self.params

        response = requests.request(self.method, **request_kwargs)
        response.raise_for_status()
        return response.json()
