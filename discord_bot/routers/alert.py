from fastapi import APIRouter 
from discord_bot.dc_bot import  bot
import discord
from dotenv import load_dotenv
import os
from datetime import datetime
from db import get_connection, Transactions

load_dotenv()
img_url = os.getenv('STOCK_IMG_URL')

router = APIRouter(
    prefix = '/alert', 
    tags= ["alert"], 
    responses={404: {"description": "Not found"}}
)

trx = Transactions()

@router.get("/")
async def rt_alert(code: str,tick_time: str, price: float, shares: int, type: int ):    
    for guild in bot.guilds:
        for channel in guild.channels:
            if channel.name == 'running-trade-detector':
                if type == 1:
                    status = 'BUY'
                    color = discord.Colour.green()
                else:
                    status = 'SELL'    
                    color = discord.Colour.red()
                    
                value = round((price * shares), 2)  

                embed = discord.Embed(
                    color=color,
                    title=f"[{status}][{code}]",
                    description=f"""
                        - TICK TIME \t: {tick_time} \n- PRICE     \t\t: {price:,}\n- LOT     \t\t\t: {round(shares/100)}\n- VALUE\t\t\t: Rp. {value:,}
                    """
                )               

                # save and caching to database
                trx.trx_cache.append((code, 
                                      datetime.strptime(tick_time,'%Y-%m-%d %H:%M:%s'), 
                                      price, shares, type))
                if len(trx.trx_cache) >= 100:
                    cursor = get_connection()
                    trx.save_transaction(cursor)

                construct_url = img_url+code+'.png'                                
                embed.set_thumbnail(url=construct_url)                    
                await channel.send(embed=embed)