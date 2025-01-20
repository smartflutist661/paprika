import gzip
import json
from collections.abc import Iterable
from typing import (
    NewType,
    Optional,
    TypedDict,
    cast,
)

from paprika_api.exceptions import PaprikaError
from paprika_api.groceries import (
    GroceryAisleId,
    Ingredient,
)
from paprika_api.paprika import PaprikaClient

PantryItemId = NewType("PantryItemId", str)
IsoDatetime = NewType("IsoDatetime", str)


class PantryItem(TypedDict):

    uid: PantryItemId
    ingredient: Ingredient
    aisle: Optional[str]
    expiration_date: Optional[IsoDatetime]
    has_expiration: bool
    in_stock: bool
    purchase_date: Optional[IsoDatetime]
    quantity: str
    aisle_uid: Optional[GroceryAisleId]
    location_uid: None
    notes: None
    deleted: bool


def get_pantry_items(client: PaprikaClient) -> list[PantryItem]:
    response = client.session.get(f"{client.base_url}/sync/pantry/")
    response.raise_for_status()
    return cast(list[PantryItem], response.json()["result"])


def post_pantry_items(client: PaprikaClient, groceries: Iterable[PantryItem]) -> None:
    data = gzip.compress(json.dumps(list(groceries)).encode("utf8"))
    response = client.session.post(f"{client.base_url}/sync/pantry/", files={"data": data})
    response.raise_for_status()
    if response.json().get("result", False) is False:
        raise PaprikaError(request=response.request)
