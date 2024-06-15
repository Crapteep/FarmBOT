from dataclasses import dataclass
import requests
import json
from helpers.helper import Helper

class Farm:
    def __init__(self, farm_id: int, position: int, buildingid: int, level: int, status: int, animals: int, product: int, name: str, client, items: list, seed: int):
        self.client = client
        self.farm_id = farm_id
        self.position = position
        self.name = name
        self.buildingid = buildingid
        self.level = level
        self.status = status
        self.animals = animals
        self.product = product
        self.items = items
        self.seed = seed
        

    def fetch_farm_data(self, url=None, params=None):
        if url is None:
            url = self.client.url

        rsp_data = None
        response = requests.get(url, headers=self.client.headers, params=params)

        if response.status_code == 200 and self.client.connected:
            if response.content == b'failed':
                self.client.connected = False
                print("Session expired")
            else:
                try:
                    rsp_data = json.loads(response.content.decode("utf-8"))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
        else:
            Helper.response(self.farm_id, self.position, "Error while fetch data")
        return rsp_data


@dataclass
class FieldData:
    field_id: int
    plant: int
    planted: int
    collection_at: int
    watered: int
    guild: int
    buildingid: int
    x: int
    y: int
    iswater: bool
    phase: int


@dataclass
class AnimalData:
    pid: int
    crop: int
    time: int
    remain: int
    rest: int
    feed: dict


@dataclass
class SlotData:
    pid: int
    remain: int
    amount: int
