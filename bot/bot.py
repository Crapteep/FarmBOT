from account.account import AccountData
import asyncio


class Bot:
    def __init__(self, headers, phpsessid, username, password, server, seed) -> None:
        self.headers = headers
        self.phpsessid = phpsessid
        self.username = username
        self.password = password
        self.server = server
        self.seed = seed


    async def run(self):
        if self.headers is None or self.phpsessid is None or self.username is None or self.password is None or self.server is None or self.seed is None:
            raise Exception(
                "Required variables are empty. Please load environment variables or provide values before running the program.")

        self.account = AccountData(headers=self.headers, phpsessid=self.phpsessid,
                                   username=self.username, password=self.password, server=self.server, seed=self.seed)

        while True:
            try:
                self.account.check_farms()
                await asyncio.sleep(60 * 10)
            except:
                await asyncio.sleep(60 * 2)
