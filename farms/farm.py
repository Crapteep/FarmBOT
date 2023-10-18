from dataclasses import dataclass

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
        

    def update(self):
        pass



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

