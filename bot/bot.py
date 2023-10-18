# from account.account import AccountData
from account import account
import time

class Bot:
    def __init__(self, headers, phpsessid, username, password, server, seed) -> None:
        self.account = account.AccountData(headers=headers, phpsessid=phpsessid, username=username, password=password, server=server, seed=seed)

    def run(self):
        while True:
            print("Checking farms..")
            for animal_farm in self.account.animalFarms:
                animal_farm.collect()

            for plant_farm in self.account.plantFarms:
                plant_farm.collect()
            print("Farm check completed.")
            time.sleep(120)

            