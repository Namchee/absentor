from discord import Game, Status
from discord.ext import commands

class AbsentorBot(commands.Cog):
    def __init__(self, bot, sheet):
        self.bot = bot
        self.sheet = sheet

    """On ready, log all guilds connected to this bot instance
    And change the status
    """
    @commands.Cog.listener()
    async def on_ready(self):
        print('Absentor is connected to these servers:')

        for guild in self.bot.guilds:
            print('{} ({})'.format(guild.name, guild.id))

        await self.bot.change_presence(
            status=Status.online,
            activity=Game(name="Absensi Mahasiswa")
        )
    
    @commands.command(name='absen')
    async def handle_absen(self, ctx, *args):
        await ctx.send('Testing')
