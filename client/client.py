import requests
from helpers.helper import Helper
import time
import threading



class Client:
    def __init__(self, headers, phpsessid, username, password, server=1, url="https://s1.wolnifarmerzy.pl/ajax/farm.php") -> None:
        self.headers = headers
        self.url = url
        self.phpsessid = phpsessid
        self._username = username
        self._password = password
        self.server = server
        self.wunr = None
        self.rid = None
        self.connected = False
        self.find_rid()
        


        self.connected_thread = threading.Thread(target=self.monitor_connected)
        self.connected_thread.daemon = True

        self.connected_thread.start()

    def find_rid(self):
        actual_time = str(time.time()).replace('.', '')

        data = {
            'server': self.server,
            'username': self._username,
            'password': self._password,
            'ref': 'up_port',
        }

        cookies = {
            'ref': 'up_port',
            'PHPSESSID': self.phpsessid,
            'wunr': self.wunr,
        }

        create_token_url = f"https://www.wolnifarmerzy.pl/ajax/createtoken2.php?n={actual_time}"

        response = requests.post(create_token_url, data=data)
        if response.status_code == 200:
            print("Successfully logged in")

            redirect_url = response.json()[1]
            self.wunr = Helper.regular_expression(redirect_url, r'unr=(\d+)')

            login_response = requests.get(redirect_url, cookies=cookies)
            content_str = login_response.content.decode('utf-8')
            self.rid = Helper.regular_expression(
                content_str, r"var rid = '([a-f0-9]+)';")
            self.update_headers()
            self.connected = True
        else:
            print("Login error")


    def update_headers(self):
        self.headers["Cookie"] = self.headers["Cookie"].format(self.phpsessid, self.wunr)


    def monitor_connected(self):
        while True:
            if self.connected is False:
                try:
                    self.find_rid()
                    print('The new rid has been set')
                except Exception as e:
                    print("ERROR: ", e)
            time.sleep(5)