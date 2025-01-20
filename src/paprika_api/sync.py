from typing import (
    Literal,
    TypedDict,
    cast,
)

from paprika_api.exceptions import PaprikaError
from paprika_api.paprika import PaprikaClient

Route = Literal[
    "categories",
    "recipes",
    "photos",
    "groceries",
    "grocerylists",
    "groceryaisles",
    "groceryingredients",
    "meals",
    "mealtypes",
    "bookmarks",
    "pantry",
    "pantrylocations",
    "menus",
    "menuitems",
]


class SyncCounters(TypedDict):
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


def get_status(client: PaprikaClient) -> SyncCounters:
    response = client.session.get(
        f"{client.base_url}/sync/status/",
        timeout=client.timeout,
    )
    response.raise_for_status()
    if response.json().get("result", False) is False:
        raise PaprikaError(request=response.request)
    return cast(SyncCounters, response.json()["result"])
