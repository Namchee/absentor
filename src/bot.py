from discord.ext import commands

class AbsentorBot(commands.Cog):
    def __init__(self, bot, sheet):
        self.bot = bot
        self.sheet = sheet
    
    @commands.command(name='absen')
    async def handle_absen(self, ctx, *args):
        await ctx.send('Testing')
