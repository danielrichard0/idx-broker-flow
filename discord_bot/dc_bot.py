import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents )

@bot.event
async def on_ready():
    print(f"we are ready to go in, {bot.user.name}")
    a = discord.Guild()

@bot.command()
async def create_channel(ctx):        
    server = ctx.guild

    channel_name = 'running-trade-detector'
    category = 'Indonesian Stocks'

    serv_categories = server.categories
    categoryObj: discord.channel.CategoryChannel 

    # servCategories is [CategoryChannel] so I need to refer to its attribute : name
    if category not in [obj.name for obj in serv_categories]:
        categoryObj = await server.create_category(name=category)
    else:
        for val in serv_categories:
            if val.name == category:
                categoryObj = val
                
    if channel_name not in [obj.name for obj in server.channels]:
        await server.create_text_channel(name=channel_name, category=categoryObj)        
    else:
        await ctx.send(f"Channel {channel_name} sudah dibuat sebelumnya!")   