import os
from typing import Any, Dict, Optional

import requests
from robot.api import logger
from robot.api.deco import keyword, library


@library(scope="GLOBAL")
class ApiHelper:
    """Robot Framework library for API authentication and session management."""

    def __init__(self) -> None:
        self.session = requests.Session()
        self.master_cache: Dict[str, Any] = {}
        self.bearer_token: Optional[str] = None

    @keyword("Create Bearer Token")
    def create_bearer_token(self) -> str:
        auth_url = os.environ.get("API_AUTH_URL")
        if not auth_url:
            base_url = os.environ.get("API_BASE_URL")
            if not base_url:
                raise RuntimeError("API_AUTH_URL or API_BASE_URL must be set")
            auth_url = base_url

        username = os.environ.get("API_USERNAME")
        password = os.environ.get("API_PASSWORD")
        if not username or not password:
            raise RuntimeError("API_USERNAME and API_PASSWORD must be set")

        payload: Dict[str, Any] = {
            "username": username,
            "password": password,
        }
        client_id = os.environ.get("API_CLIENT_ID")
        if client_id:
            payload["client_id"] = client_id

        response = self.session.post(auth_url, json=payload, timeout=10)
        logger.info(f"Authenticating against {auth_url}")
        logger.info(f"Authentication response status: {response.status_code}")
        response.raise_for_status()

        response_data = response.json()
        token = (
            response_data.get("access_token")
            or response_data.get("accessToken")
            or response_data.get("token")
            or response_data.get("id_token")
            or response_data.get("data", {}).get("access_token")
            or response_data.get("data", {}).get("accessToken")
            or response_data.get("data", {}).get("token")
        )
        if not token:
            raise AssertionError(
                "Login response did not contain access_token, token, or id_token"
            )

        self.bearer_token = str(token)
        self.master_cache["ACCESS_TOKEN"] = self.bearer_token
        self.master_cache["AUTH_RESPONSE"] = response_data
        logger.info("Bearer token created and stored in master_cache[ACCESS_TOKEN]")
        self.session.headers.update(
            {"Authorization": f"Bearer {self.bearer_token}"}
        )
        return self.bearer_token

    @keyword("Get Access Token")
    def get_access_token(self) -> str:
        token = self.master_cache.get("ACCESS_TOKEN")
        if not token:
            raise AssertionError("Bearer token has not been created")
        return str(token)

    @keyword("Get Master Cache")
    def get_master_cache(self) -> Dict[str, Any]:
        return self.master_cache

    @keyword("Get Master Cache Value")
    def get_master_cache_value(self, key: str) -> Any:
        if key not in self.master_cache:
            raise KeyError(f"Master cache does not contain '{key}'")
        return self.master_cache[key]

    @keyword("Print Master Cache")
    def print_master_cache(self) -> None:
        message = f"master_cache after update: {self.master_cache}"
        logger.info(message)
        logger.console(message)

    @keyword("Get Authenticated User")
    def get_authenticated_user(
        self, url: str, bearer_token: str
    ) -> Dict[str, Any]:
        response = self.session.get(
            url,
            headers={"Authorization": f"Bearer {bearer_token}"},
            timeout=10,
        )
        logger.info(f"GET {url} response status: {response.status_code}")
        response.raise_for_status()
        response_data = response.json()
        self.master_cache["AUTH_ME_RESPONSE"] = response_data
        logger.info("Authenticated user response stored in master_cache[AUTH_ME_RESPONSE]")
        return response_data

    @keyword("Close API Session")
    def close_api_session(self) -> None:
        self.session.close()
        logger.info("API session closed")
