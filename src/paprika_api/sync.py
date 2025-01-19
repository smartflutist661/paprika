from typing import (
    TypedDict,
    cast,
)

from paprika_api.paprika import PaprikaClient


class SyncResponse(TypedDict):
    categories: int
    recipes: int
    photos: int
    groceries: int
    grocerylists: int
    groceryaisles: int
    groceryingredients: int
    meals: int
    mealtypes: int
    bookmarks: int
    pantry: int
    pantrylocations: int
    menus: int
    menuitems: int


def get_status(client: PaprikaClient) -> SyncResponse:
    response = client.session.get(
        f"{client.base_url}/sync/status/",
        timeout=client.timeout,
    )
    response.raise_for_status()
    return cast(SyncResponse, response.json()["result"])
