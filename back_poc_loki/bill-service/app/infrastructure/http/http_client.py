from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class HttpClient(object):
    api_host: str
    _session: Optional[requests.Session] = None  # type: ignore

    def __post_init__(self):
        if not self._session:
            self._session = requests.Session()

    def get(
        self,
        endpoint: str,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        headers = {
            'Content-Type': 'application/json',
        }

        url = '{api_host}{endpoint}'.format(
            api_host=self.api_host,
            endpoint=endpoint,
        )

        print(f"apiUrl - {url}")

        response = self._session.get(  # type: ignore
            url,
            headers=headers,
            params=query_params,
        )

        print(f"jsonResponse - {response.json()}")

        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, payload: dict | str) -> Dict[str, Any]:
        headers = {
            'Content-Type': 'application/json',
        }
        url = '{api_host}{endpoint}'.format(
            api_host=self.api_host,
            endpoint=endpoint,
        )
        if isinstance(payload, dict):
            response = self._session.post(  # type: ignore
                url,
                headers=headers,
                json=payload,
            )
        elif isinstance(payload, str):
            response = self._session.post(  # type: ignore
                url,
                headers=headers,
                data=payload,
            )

        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = {
            'Content-Type': 'application/json',
        }
        url = '{api_host}{endpoint}'.format(
            api_host=self.api_host,
            endpoint=endpoint,
        )
        response = self._session.put(  # type: ignore
            url,
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()
