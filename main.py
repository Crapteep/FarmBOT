from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from bot.bot import Bot
import os
from dotenv import load_dotenv
import asyncio



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


load_dotenv()
username = os.getenv("NICKNAME")
password = os.getenv("PASSWORD")
server = os.getenv("SERVER", 1)
phpsessid = os.getenv("PHPSESSID")
seed = int(os.getenv("SEED", 8))


app = FastAPI()

origins = [
    'http://localhost:3000',
    'http://localhost:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def start_farm():
    bot = Bot(headers=headers, phpsessid=phpsessid, username=username, password=password, server=server, seed=seed)
    await bot.run()


@app.on_event("startup")
async def on_startup():
    loop = asyncio.get_event_loop()
    task = loop.create_task(start_farm())

@app.get('/')
async def index():
    return {"name": "FarmBOT",
            "author": "Crapteep"}

