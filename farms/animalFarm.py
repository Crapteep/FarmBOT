from farms.farm import Farm, AnimalData
from helpers.helper import Helper
import requests
import json



class AnimalFarm(Farm):
    def __init__(self, farm_id, position, buildingid, level, status, animals, product, name, client, items, seed):
        super().__init__(farm_id, position, buildingid, level,
                         status, animals, product, name, client, items, seed)
        self.animalsData = None
        self.update()


    def update(self):
        self.animalsData = self.init_farm()


    def collect(self):
        self.collect_items()
        self.feed()
        self.update()


    def init_farm(self):
        params = {
            "rid": self.client.rid,
            "mode": "inner_init",
            "farm": self.farm_id,
            "position": self.position,
        }

        response = requests.get(
            self.client.url, headers=self.client.headers, params=params)
        
        if response.status_code == 200:
            rsp_data = json.loads(response.content.decode("utf-8"))
            farm_data = rsp_data['datablock'][1]

            for value in farm_data.values():
                for data in value.values():
                    remain = data.get("remain")
                    if remain is None:
                        remain = 1
                    animal = AnimalData(
                        pid=data["pid"],
                        crop=data["crop"],
                        time=data["time"],
                        remain=remain,
                        rest=data["rest"],
                        feed=data["feed"],
                    )

            return animal

        else:
            Helper.response(self.farm_id, self.position, "Error while loading farm")
        

    def collect_items(self):
        params = {
            "rid": self.client.rid,
            "mode": "inner_crop",
            "farm": self.farm_id,
            "position": self.position,
        }

        if self.animalsData.remain == 1:
            response = requests.get(
                self.client.url, headers=self.client.headers, params=params)

            if response.status_code == 200:
                Helper.response(self.farm_id, self.position, "Animal products have been collected")
            else:
                Helper.response(self.farm_id, self.position, "Error while loading animal farm")


    def feed(self):
        if self.animalsData.rest > 0:
            feed_items = self.animalsData.feed.items()
            sorted_feed_items = sorted(feed_items, key=lambda item: item[1]["time"], reverse=True)

            food_index = None
            max_value = None
            amount = None

            for _, (item_index, item_data) in enumerate(sorted_feed_items):
                food_index = item_index
                max_value = item_data
                food_time = max_value["time"]

                amount = self.animalsData.rest // food_time
                available_amount = self.get_item_amount(food_index)

                if available_amount >= amount:
                    break

                elif 0 < available_amount < amount:
                    amount = available_amount

            params = {
                "rid": self.client.rid,
                "mode": "inner_feed",
                "farm": self.farm_id,
                "position": self.position,
                "pid": food_index,
                "c": f"{food_index}_{amount}|",
                "amount": amount,
                "guildjob": 0
            }

            response = requests.get(
                self.client.url, headers=self.client.headers, params=params)

            if response.status_code == 200:
                Helper.response(self.farm_id, self.position, "All the animals have been fed")
            else:
                Helper.response(self.farm_id, self.position, "Error in feeding animals on the farm")


    def get_item_amount(self, pid):
        found_item = [item for item in self.items if isinstance(
            item, dict) and item.get('pid') == pid]

        if found_item:
            return int(found_item[0]["amount"])
        return 0