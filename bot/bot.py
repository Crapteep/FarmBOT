# from account.account import AccountData
from account import account
import time

class Bot:
    def __init__(self, headers, phpsessid, username, password, server, seed) -> None:
        self.headers = headers
        self.phpsessid = phpsessid
        self.username = username
        self.password = password
        self.server = server
        self.seed = seed

    def run(self):
        self.account = account.AccountData(headers=self.headers, phpsessid=self.phpsessid, username=self.username, password=self.password, server=self.server, seed=self.seed)
        while True:
            try:
                print("Checking farms..")
                for animal_farm in self.account.animalFarms:
                    animal_farm.collect()

                for plant_farm in self.account.plantFarms:
                    plant_farm.collect()
                print("Farm check completed.")
                time.sleep(120)
            except:
                time.sleep(60)
                self.account = account.AccountData(headers=self.headers, phpsessid=self.phpsessid, username=self.username, password=self.password, server=self.server, seed=self.seed)

            