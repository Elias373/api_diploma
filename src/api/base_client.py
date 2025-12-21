import json

import allure
import requests

from src.config import APIConfig


class BaseAPIClient:
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("DELETE", endpoint, **kwargs)

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.config.base_url}{endpoint}"

        if "timeout" not in kwargs:
            kwargs["timeout"] = self.config.timeout

        response = self.session.request(method, url, **kwargs)

        self._log_to_allure(method, endpoint, url, kwargs, response)

        return response

    def _log_to_allure(self, method: str, endpoint: str, url: str,
                       kwargs: dict, response: requests.Response) -> None:
        request_body = kwargs.get("json") or kwargs.get("data")
        allure.attach(
            json.dumps({
                "method": method,
                "endpoint": endpoint,
                "url": url,
                "headers": dict(self.session.headers),
                "body": request_body
            }, indent=2, ensure_ascii=False),
            name=f"Request: {method} {endpoint}",
            attachment_type=allure.attachment_type.JSON,
        )

        allure.attach(
            response.text,
            name=f"Response {method} {endpoint}: {response.status_code}",
            attachment_type=allure.attachment_type.TEXT,
        )

