import discord
from discord.ext import commands
from common import Common
from common import ERROR_MESSAGE

class NodesCog(commands.Cog, name="Nodes"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='node', help="Displays summary of node information")
    async def node(self,ctx):
        try:
            account = await Common.get_value(ctx,'nanoNodeAccount')
            version = await Common.get_value(ctx,'version')
            dbase = await Common.get_value(ctx,'store_vendor')
            numPeers = await Common.get_value(ctx,'numPeers')
            response = (
                f"**Address:** {account}\n"
                f"**Version:** {version}\n"
                f"**DBASE:** {dbase}\n"
                f"**Number of Peers:**: {numPeers}\n"
            )
            await ctx.send(response)
        except Exception as e:
            Common.logger.error("Exception occured processing request", exc_info=True)
            await ctx.send(ERROR_MESSAGE)     

    @commands.command(name='address', aliases=['addr','node_address','nodeaddress'], help="Displays node address")
    async def address(self,ctx):
        try:
            value = await Common.get_value(ctx,'nanoNodeAccount')
            response = f"Node address is {value}"
            await ctx.send(response)
        except Exception as e:
            Common.logger.error("Exception occured processing request", exc_info=True)
            await ctx.send(ERROR_MESSAGE)  

    @commands.command(name='version', aliases=['ver'], help="Displays node version")
    async def version(self,ctx):
        try:
            value = await Common.get_value(ctx,'version')
            response = f"Node version is {value}"
            await ctx.send(response)
        except Exception as e:
            Common.logger.error("Exception occured processing request", exc_info=True)
            await ctx.send(ERROR_MESSAGE)  

    @commands.command(name='num_peers', aliases=['numpeers','peers'], help="Displays number of peers")
    async def num_peers(self,ctx):
        try:
            value = await Common.get_value(ctx,'numPeers')
            response = f"{value} peers"
            await ctx.send(response)
        except Exception as e:
            Common.logger.error("Exception occured processing request", exc_info=True)
            await ctx.send(ERROR_MESSAGE)  

    @commands.command(name='uptime', aliases=['up','nodeuptime','node_uptime'], help="Displays node uptime")
    async def uptime(self,ctx):
        try:
            value = await Common.get_value(ctx,'nodeUptimeStartup')
            pretty_node_uptime = Common.get_days_from_secs(value)
            response = f"Node uptime is {pretty_node_uptime}"
            await ctx.send(response)
        except Exception as e:
            Common.logger.error("Exception occured processing request", exc_info=True)
            await ctx.send(ERROR_MESSAGE)  

def setup(bot):
    bot.add_cog(NodesCog(bot))