from typing import (
    NewType,
    TypedDict,
    cast,
)

import requests
from requests.exceptions import HTTPError

ApiToken = NewType("ApiToken", str)


class LoginData(TypedDict):
    token: ApiToken


class LoginResponse(TypedDict):
    result: LoginData


def login(client: "PaprikaClient", email: str, password: str) -> LoginResponse:
    login_resp = client.session.post(
        f"{client.base_url}/account/login",
        data={"email": email, "password": password},
        timeout=client.timeout,
    )
    login_resp.raise_for_status()
    login_json = login_resp.json()
    if login_json.get("result", {}).get("token", None) is None:
        login_resp.status_code = 401
        raise HTTPError(response=login_resp)

    return cast(LoginResponse, login_json)


class PaprikaClient:
    session: requests.Session
    timeout: int  # seconds
    base_url: str
    user_agent: str
    api_token: ApiToken

    def __init__(self, email: str, password: str, timeout: int = 5) -> None:
        self.session = requests.Session()
        self.base_url = "https://www.paprikaapp.com/api/v2"
        self.user_agent = "Paprika 3/3.8.2 (com.hindsightlabs.paprika.ios.v3; build:71; iOS 18.1.1) Alamofire/5.2.2"
        self.timeout = timeout

        self.session.headers = {"user-agent": self.user_agent}

        self.api_token = login(self, email, password)["result"]["token"]

        self.session.headers |= {
            "authorization": f"Bearer {self.api_token}",
        }
