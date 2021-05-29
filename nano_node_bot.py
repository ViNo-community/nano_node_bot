# Nano Discord bot

import asyncio
import json
import os
import discord
import requests
import logging
import datetime
from pathlib import Path
from dotenv import load_dotenv
from discord.ext import commands

# Nano node RPC document: https://docs.nano.org/commands/rpc-protocol/

# Set up logging
filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_nano_node_bot.log"
logdir = Path(__file__).resolve().parent / "logs" 
# Make directory if it doesn't already exist
if not os.path.exists(logdir):
    try:
        os.makedirs(logdir)
    except OSError as e:
        print(f"Error creating {logdir} :", e)
        exit()
logfile = logdir / filename
logging.basicConfig(filename=logfile, format='%(asctime)-10s - %(levelname)s - %(message)s', level=logging.INFO)

# Load discord token from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')
RPC_URL = os.getenv('RPC_URL')

# Helper function for logging
# {User} requests {command}
def logit(ctx):
    print(f"{ctx.message.author} requests {ctx.command}")
    logging.info(f"{ctx.message.author} requests {ctx.command}")

# Initiate Discord bot
bot = commands.Bot(command_prefix='.')

# Bot is ready
@bot.event
async def on_ready():
    # Log successful connection
    logging.info(f"{bot.user.name} connected")
    print(f"{bot.user.name} connected. Log file:", logfile)

# Helper function for getting value from JSON response
async def get_value(ctx, param):
    answer = ""
    try:
        # Log query
        logit(ctx)
        # Grab response from RPC_URL
        r = requests.get(RPC_URL, timeout=2.50)
        # Parse JSON
        content = json.loads(r.text)
        # Grab value named param
        answer = content[param]
        # Log answer
        logging.info(f"Answer: {answer}")
    except Exception as ex:
        # Log exception with stack trace
        logging.error("Exception occured", exc_info=True)
    return answer

# TODO: Put into Node cog - version, uptime, server_uptime
####

@bot.command(name='version', help="Displays node version")
async def version(ctx):
    value = await get_value(ctx,'version')
    response = f"Node version is {value}"
    await ctx.send(response)

@bot.command(name='uptime', help="Displays node uptime")
async def uptime(ctx):
    value = await get_value(ctx,'nodeUptimeStartup')
    time = int(value)
    # Break down into days, hours, minutes, seconds
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hours = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    response = f"Node uptime is {day} days, {hours} hours, {minutes} minutes, and {seconds} seconds"
    await ctx.send(response)

@bot.command(name='server_uptime', help="Displays server uptime")
async def server_uptime(ctx):
    value = await get_value(ctx,'systemUptime')
    response = f"Server uptime is {value}"
    await ctx.send(response)
####

# TODO: Put into Accounts cog - balance, representative, num_peers, voting_weight
####

@bot.command(name='balance', help="Displays account balance")
async def balance(ctx):
    value = await get_value(ctx,'accBalanceMnano')
    response = f"Account balance is {value:.2f} nano"
    await ctx.send(response)

@bot.command(name='representative', help="Displays representative")
async def representative(ctx):
    value = await get_value(ctx,'repAccount')
    response = f"Representative: {value}"
    await ctx.send(response)

@bot.command(name='num_peers', help="Displays number of peers")
async def num_peers(ctx):
    value = await get_value(ctx,'numPeers')
    response = f"{value} peers"
    await ctx.send(response)

@bot.command(name='voting_weight', help="Displays voting weight")
async def voting_weight(ctx):
    value = await get_value(ctx,'votingWeight')
    response = f"Voting weight is {value:.2f} nano"
    await ctx.send(response)

####

#TODO: Put into Blocks cog - current_block, cemented_blocks, unchecked_blocks, sync
###

@bot.command(name='current_block', help="Displays the current block")
async def current_block(ctx):
    value = await get_value(ctx,'currentBlock')
    response = f"Current block is {value}"
    await ctx.send(response)

@bot.command(name='cemented_blocks', help="Displays the cemented block count")
async def cemented_blocks(ctx):
    value = await get_value(ctx,'cementedBlocks')
    response = f"Cemented block count is {value}"
    await ctx.send(response)

@bot.command(name='unchecked_blocks', help="Displays the number of unchecked blocks")
async def unchecked_blocks(ctx):
    value = await get_value(ctx,'uncheckedBlocks')
    response = f"{value} unchecked blocks"
    await ctx.send(response)

@bot.command(name='sync', help="Displays block sync")
async def block_sync(ctx):
    value = await get_value(ctx,'blockSync')
    response = f"Block sync is {value}%"
    await ctx.send(response)

###    

# Command not found. Not a big deal, log it and ignore it.
@bot.event
async def on_command_error(ctx, error):
    print(f"{ctx.message.author} tried {ctx.invoked_with} Error: ", error)
    logging.info(f"{ctx.message.author} tried {ctx.invoked_with} Error: {error}")

# Run the bot
bot.run(DISCORD_TOKEN)