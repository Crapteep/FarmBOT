from farms.plantFarm import PlantFarm
from farms.animalFarm import AnimalFarm
from client.client import Client
import requests
import json


class AccountData(Client):
    FARM_TYPES = {
        "Pole": PlantFarm,
        "Kurnik": AnimalFarm,
        "Obora": AnimalFarm,
        "Owczarnia": AnimalFarm,
        "Kozia chatka": AnimalFarm
    }

    def __init__(self, headers, phpsessid, username, password, server, seed):
        super().__init__(headers=headers, phpsessid=phpsessid,
                         username=username, password=password, server=server)
        self.plantFarms = []
        self.animalFarms = []
        self.seed = seed
        self.items = []
        self.init_farms()

    def init_farms(self):
        params = {
            "rid": self.rid,
            "mode": "getfarms",
            "farm": "1",
            "position": "0",
        }

        response = requests.get(self.url, headers=self.headers, params=params)

        if response.status_code == 200:
            rsp_data = json.loads(response.content.decode("utf-8"))
            farms_data = rsp_data['updateblock']['farms']['farms']
            items_data = rsp_data["updateblock"]["stock"]["stock"]["1"]
            for items in items_data.values():
                for val in items.values():
                    self.items.append(val)

            for farm_id, farms in farms_data.items():
                for _, farm in farms.items():
                    farm_type = farm["name"]
                    farm_class = self.FARM_TYPES.get(farm_type)

                    if farm_class:
                        farm_instance = farm_class(
                            client=self,
                            farm_id=farm_id,
                            name=farm["name"],
                            position=farm["position"],
                            buildingid=farm["buildingid"],
                            level=farm["level"],
                            status=farm["status"],
                            animals=farm["animals"],
                            product=farm["product"],
                            items=self.items,
                            seed=self.seed
                        )
                        if farm_type == "Pole":
                            self.plantFarms.append(farm_instance)
                        else:
                            self.animalFarms.append(farm_instance)
        else:
            print("Error while loading farms")

    def check_farms(self):
        if self.connected:
            print("Checking farms..")
            for animal_farm in self.animalFarms:
                animal_farm.collect()
            for plant_farm in self.plantFarms:
                plant_farm.collect()
            print("Farm check completed.")