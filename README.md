# UNOFFICIAL SDK for Paprika Recipe Manager

An unofficial SDK for the Paprika Recipe Manager API.
Currently handles Groceries and Pantry sections.

## Usage

Log in with the `PaprikaClient`:
 
```python
client = PaprikaClient(email=<your-email>, password=<your-password>)
```

The Paprika API currently rejects login requests from "unrecognized clients".
The client therefore currently uses an iOS user agent, though this is not required
after an API token has been acquired.

## TODO

The routes below are polled on a forced sync, but not currently available in this SDK.
There may be additional routes not noted below.

* Bookmarks
* Categories
* Recipes
* Meals
  * Mealtypes
  * Meals
* Menus
  * Menus
  * Menuitems
* Photos
