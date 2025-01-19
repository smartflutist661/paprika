from paprika_api.exceptions import PaprikaError
from paprika_api.paprika import PaprikaClient


def notify(client: PaprikaClient) -> None:
    response = client.session.post(
        f"{client.base_url}/sync/notify/",
        headers=dict(client.session.headers) | {"content-length": "0"},
    )
    response.raise_for_status()
    if response.json().get("result", False) is False:
        raise PaprikaError(request=response.request)
