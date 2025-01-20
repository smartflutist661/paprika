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
from paprika_api.paprika import PaprikaClient

GroceryListId = NewType("GroceryListId", str)
GroceryId = NewType("GroceryId", str)
GroceryAisleId = NewType("GroceryAisleId", str)
GroceryIngredientId = NewType("GroceryIngredientId", str)

Ingredient = NewType("Ingredient", str)
AisleName = NewType("AisleName", str)
ListName = NewType("ListName", str)


class GroceryAisle(TypedDict):
    uid: GroceryAisleId
    name: AisleName
    order_flag: Optional[int]
    deleted: bool


class GroceryList(TypedDict):
    uid: GroceryListId
    name: ListName
    order_flag: Optional[int]
    is_default: bool
    reminders_list: Optional[str]
    deleted: bool


class Grocery(TypedDict):
    """
    recipe_uid:
        Always None, even when `recipe` is populated
    name:
        This shows up in the Items section of the Ingredient if there is more than one.
        By default, a combination of `ingredient` and `instruction`
    ingredient:
        This is what actually appears in the list; pseudo-unique identifier
    quantity:
        A string that includes units
    instruction:
        Notes
    """

    uid: GroceryId
    recipe_uid: None
    name: str
    order_flag: Optional[int]
    purchased: bool
    aisle: Optional[str]
    ingredient: Ingredient
    recipe: Optional[str]
    instruction: str
    quantity: str
    separate: bool
    aisle_uid: Optional[GroceryAisleId]
    list_uid: Optional[GroceryListId]
    deleted: bool


class GroceryIngredient(TypedDict):
    uid: GroceryIngredientId
    name: Ingredient
    aisle_uid: Optional[GroceryAisleId]
    deleted: bool


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


def post_groceries(client: PaprikaClient, groceries: Iterable[Grocery]) -> None:
    data = gzip.compress(json.dumps(list(groceries)).encode("utf8"))
    response = client.session.post(
        f"{client.base_url}/sync/groceries/",
        files={"data": data},
    )
    response.raise_for_status()
    if response.json().get("result", False) is False:
        raise PaprikaError(request=response.request)


def get_grocery_aisles(client: PaprikaClient) -> list[GroceryAisle]:
    response = client.session.get(f"{client.base_url}/sync/groceryaisles/")
    response.raise_for_status()
    return cast(list[GroceryAisle], response.json()["result"])


def post_grocery_aisles(client: PaprikaClient, grocery_aisles: Iterable[GroceryAisle]) -> None:
    data = gzip.compress(json.dumps(list(grocery_aisles)).encode("utf8"))
    response = client.session.post(
        f"{client.base_url}/sync/groceryaisles/",
        files={"data": data},
    )
    response.raise_for_status()
    if response.json().get("result", False) is False:
        raise PaprikaError(request=response.request)


def get_grocery_ingredients(client: PaprikaClient) -> list[GroceryIngredient]:
    response = client.session.get(f"{client.base_url}/sync/groceryingredients/")
    response.raise_for_status()
    return cast(list[GroceryIngredient], response.json()["result"])


def post_grocery_ingredients(
    client: PaprikaClient,
    grocery_ingredients: Iterable[GroceryIngredient],
) -> None:
    data = gzip.compress(json.dumps(list(grocery_ingredients)).encode("utf8"))
    response = client.session.post(
        f"{client.base_url}/sync/groceryingredients/",
        files={"data": data},
    )
    response.raise_for_status()
    if response.json().get("result", False) is False:
        raise PaprikaError(request=response.request)
