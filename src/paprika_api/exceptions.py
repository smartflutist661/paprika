from requests.exceptions import HTTPError


class PaprikaError(HTTPError):
    """An unknown error occurred in the request"""
