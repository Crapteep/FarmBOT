from bot.bot import Bot
import os
from dotenv import load_dotenv

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pl",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "PHPSESSID={}; ref=up_port; wunr={};",
    "DNT": "1",
    "Host": "s1.wolnifarmerzy.pl",
    "If-Modified-Since": "Sat, 1 Jan 2000 00:00:00 GMT",
    "Pragma": "no-cache",
    "Referer": "https://s1.wolnifarmerzy.pl/main.php?ref=up_port",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows"
}


if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("NICKNAME")
    password = os.getenv("PASSWORD")
    server = os.getenv("SERVER")
    phpsessid = os.getenv("PHPSESSID")

    bot = Bot(headers=headers, phpsessid=phpsessid, username=username, password=password, server=server, seed=17)
    bot.run()