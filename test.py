import json
import os

import requests

local = True
port = 8080

if local:
    url = f"http://127.0.0.1:{port}"
else:
    url = os.environ["ENDPOINT"]


def register(item: dict):
    print(f"Register {item['uid']}: ", end="")
    response = requests.post(f"{url}/register", data=item)
    print(response.status_code)


def unregister(uid: str):
    print(f"Unregister {uid}: ", end="")
    response = requests.delete(f"{url}/unregister", params={"uid": uid})
    print(response.status_code)


def get(uid: str):
    print(f"Get {uid}: ", end="")
    response = requests.get(f"{url}/item", params={"uid": uid})
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        data = response.text
        print(response.status_code)


def get_catalog():
    print("Get Catalog:")
    response = requests.get(f"{url}/catalog")
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        data = response.text
        print(response.status_code)


service1 = {
    "uid": "service1",
    "endpoint": "https://endpoint",
    "documentation": "https://documentation"
}
service2 = {
    "uid": "service2",
    "endpoint": "https://endpoint2",
    "documentation": "https://documentation2"
}

get_catalog()
register(service1)
get(service1["uid"])
register(service2)
get_catalog()
unregister(service1["uid"])
get(service1["uid"])
get_catalog()
