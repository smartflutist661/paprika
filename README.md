# UNOFFICIAL SDK for Paprika Recipe Manager

An unofficial SDK for the Paprika Recipe Manager API.

## Usage

Log in with the `PaprikaClient`:
 
```python
client = PaprikaClient(email=<your-email>, password=<your-password>)
```

The Paprika API currently rejects login requests from "unrecognized clients".
The client therefore currently uses an iOS user agent.
