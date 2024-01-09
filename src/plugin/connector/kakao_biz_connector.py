import json
import http.client
import requests
import logging
from spaceone.core.connector import BaseConnector

from plugin.error.https import ERROR_CLIENT_REQUEST_FAILED, ERROR_SERVER_FAILED

_LOGGER = logging.getLogger(__name__)

_DEFAULT_URL = f"https://api.megabird.co.kr:8080/v1/openapi"


class KakaoBizConnector(BaseConnector):
    def send_message(self, data: dict, headers: dict) -> None:
        url = f"{_DEFAULT_URL}/alimtalk/send"
        res = requests.post(url, data=json.dumps(data), headers=headers)
        if res.status_code != 200:
            self._handle_https_error(res.status_code, res.text)

    @staticmethod
    def _handle_https_error(status_code: int, reason: str) -> None:
        if status_code == 503 or status_code == 500:
            # all 5xx errors are handled here
            raise ERROR_SERVER_FAILED(status_code=status_code, reason=reason)
        else:
            # all 4xx errors are handled here
            raise ERROR_CLIENT_REQUEST_FAILED(status_code=status_code, reason=reason)
