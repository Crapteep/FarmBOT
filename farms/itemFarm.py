from farms.farm import Farm
from helpers.helper import Helper
from datetime import datetime


class ItemFarm(Farm):
    def __init__(self, farm_id, position, buildingid, level, status, animals, product, name, client, items, seed):
        super().__init__(farm_id, position, buildingid, level,
                         status, animals, product, name, client, items, seed)
        self.slots = None
        self.update()


    def update(self):
        self.slots = self.init_farm()


    def collect(self):
        self.update()
        self.collect_items()
        self.start_production(1)


    def init_farm(self):
        params = {
            "rid": self.client.rid,
            "mode": "innerinfos",
            "farm": self.farm_id,
            "position": self.position,
        }

        rsp_data = self.fetch_farm_data(params=params)

        if rsp_data is not None:
            farm_data = rsp_data['datablock'][1]
            slots = farm_data["slots"]
            return slots
        return None


    def collect_items(self):
        for key, slot in self.slots.items():
            if "ready" in slot and slot['ready'] == 1:
                slot_id = key

                params = {
                    "rid": self.client.rid,
                    "mode": "harvestproduction",
                    "farm": self.farm_id,
                    "position": self.position,
                    "id": 1,
                    "slot": slot_id
                }

                rsp_data = self.fetch_farm_data(params=params)
                if rsp_data is not None:
                    self.update()
                    Helper.response(self.farm_id, self.position, f"Products from {self.name} have been collected")
                else:
                    Helper.response(self.farm_id, self.position, f"Products in {self.name} are not ready yet")
            elif "remain" in slot:
                if isinstance(slot['remain'], int):
                    remain_hours = slot['remain'] // 3600
                    remain_minutes = (slot['remain'] % 3600) // 60
                    remain_seconds = slot['remain'] % 60
                    
                    remain_str = f"{remain_hours} hours, {remain_minutes} minutes, {remain_seconds} seconds"
                    
                    Helper.response(self.farm_id, self.position, f"A collection of products from the {self.name} will be available for {remain_str}.")
                else:
                    print(f"Unexpected type for slot['remain']: {type(slot['remain'])}")
                    Helper.response(self.farm_id, self.position, f"Unexpected data format for remaining time in {self.name}")



    def start_production(self, product_id):
        for key, slot in self.slots.items():
            if not slot:
                slot_id = key
                params = {
                    "rid": self.client.rid,
                    "farm": self.farm_id,
                    "position": self.position,
                    "slot": slot_id,
                    "item": product_id,
                    "mode": "start"
                }

                rsp_data = self.fetch_farm_data(params=params)
                if rsp_data is not None:
                    self.update()
                    Helper.response(self.farm_id, self.position, f"Production in {self.name} has started.")
                else:
                    Helper.response(self.farm_id, self.position, f"Previous production not yet finished")
