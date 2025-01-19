import gzip
import json
from collections.abc import Iterable
from typing import (
    NewType,
    TypedDict,
    cast,
)

from paprika_api.exceptions import PaprikaError
from paprika_api.paprika import PaprikaClient

GroceryListId = NewType("GroceryListId", str)
GroceryId = NewType("GroceryId", str)
GroceryAisleId = NewType("GroceryAisleId", str)
GroceryIngredientId = NewType("GroceryIngredientId", str)


class GroceryAisle(TypedDict):
    uid: GroceryAisleId
    name: str
    order_flag: int


class GroceryList(TypedDict):
    uid: GroceryListId
    name: str
    order_flag: int
    is_default: bool
    reminders_list: str


class Grocery(TypedDict):
    """
    recipe_uid:
        Always None, even when `recipe` is populated
    name:
        This shows up in the Items section of the Ingredient if there is more than one
    ingredient:
        This is what actually appears in the list
    quantity:
        A string that includes units
    """

    uid: GroceryId
    recipe_uid: None
    name: str
    order_flag: int
    purchased: bool
    aisle: str
    ingredient: str
    recipe: str
    instruction: str
    quantity: str
    separate: bool
    aisle_uid: GroceryAisleId
    list_uid: GroceryListId


class GroceryIngredient(TypedDict):
    uid: GroceryIngredientId
    name: str
    aisle_uid: GroceryAisleId


def get_grocery_lists(client: PaprikaClient) -> list[GroceryList]:
    response = client.session.get(f"{client.base_url}/sync/grocerylists/")
    response.raise_for_status()
    return cast(list[GroceryList], response.json()["result"])


def post_grocery_lists(client: PaprikaClient, grocery_lists: Iterable[GroceryList]) -> None:
    data = gzip.compress(json.dumps(list(grocery_lists)).encode("utf8"))
    response = client.session.post(
        f"{client.base_url}/sync/grocerylists/",
        files={"data": data},
    )
    response.raise_for_status()
    if response.json().get("result", False) is False:
        raise PaprikaError(request=response.request)


def get_groceries(client: PaprikaClient) -> list[Grocery]:
    response = client.session.get(f"{client.base_url}/sync/groceries/")
    response.raise_for_status()
    return cast(list[Grocery], response.json()["result"])


def get_grocery_aisles(client: PaprikaClient) -> list[GroceryAisle]:
    response = client.session.get(f"{client.base_url}/sync/groceryaisles/")
    response.raise_for_status()
    return cast(list[GroceryAisle], response.json()["result"])


def get_grocery_ingredients(client: PaprikaClient) -> list[GroceryIngredient]:
    response = client.session.get(f"{client.base_url}/sync/groceryingredients/")
    response.raise_for_status()
    return cast(list[GroceryIngredient], response.json()["result"])


def post_groceries(client: PaprikaClient, groceries: Iterable[Grocery]) -> None:
    data = gzip.compress(json.dumps(list(groceries)).encode("utf8"))
    response = client.session.post(
        f"{client.base_url}/sync/groceries/",
        files={"data": data},
    )
    response.raise_for_status()
    if response.json().get("result", False) is False:
        raise PaprikaError(request=response.request)
