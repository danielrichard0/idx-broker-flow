from fastapi import FastAPI
from discord_bot.dc_bot import  bot
import discord 
import asyncio
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from routers import alert

load_dotenv()
token = os.getenv('DISCORD_KEY')

@asynccontextmanager
async def lifespan(app: FastAPI):    
    asyncio.create_task(bot.start(token))
    await asyncio.sleep(3)
    print(f"{bot.user} is connected to Discord!")
    yield   

app = FastAPI(lifespan=lifespan)     
app.include_router(alert.router)