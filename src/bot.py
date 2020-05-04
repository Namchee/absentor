from threading import Timer
from discord import Game, Status
from discord.ext import commands
from src.model.server import Server

class AbsentorBot(commands.Cog):
    def __init__(self, bot, sheet):
        self.bot = bot
        self.sheet = sheet

        self.servers = {}

    """On ready, register all guilds state connected to this bot
    And change the status
    """
    @commands.Cog.listener()
    async def on_ready(self):
        print('Absentor is currently connected on:')

        for guild in self.bot.guilds:
            # Harusnya hanya print ajah, ini pengganti @everyone
            target_role = None

            for role in guild.roles:
                if role.name == '@siswa':
                    target_role = role
                    break

            self.servers[guild.id] = Server(target_role)

            print('{} - <{}>'.format(guild.name, guild.id))

        await self.bot.change_presence(
            status=Status.online,
            activity=Game(name='Absensi Mahasiswa')
        )

    """Create a group of commands called absentor
    """
    @commands.group(name='absentor')
    async def absentor(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                'Maaf {}, tapi perintah tersebut tidak dapat dipahami 🤔'.format(ctx.author.mention)
            )

    """Invoke a command to initiate an absen session.
        Will fail if the invoker is not the guild owner or doesn't have @botadmin role.
        Parameters:
            - time {int}: Time limit for an absen session
    """
    @absentor.command(name='mulai')
    @commands.has_role('@botadmin')
    async def handle_mulai(self, ctx, time: int = 15):
        server = self.servers[ctx.guild.id]

        if server.timer != None:
            await ctx.send(
                'Maaf {}, namun telah ada sesi absen yang sedang berlangsung pada server ini 😥'.format(ctx.author.mention)
            )
            await ctx.send('Silahkan menunggu sesi absen tersebut selesai.')

            return
        else:
            timer = Timer(time * 60, self.write_to_sheet, ctx)

            server.start_absen(timer)

            await ctx.send(
                '{}, sesi absen sedang dimulai. Segera lakukan absensi dengan mengirimkan pesan `!absentor absen` pada server ini dan tetap _online_ sampai sesi absen selesai.'.format(server.role.mention)
            )
            await ctx.send('Waktu absen = {} menit'.format(time))

    @absentor.command(name='berhenti')
    @commands.has_role('@botadmin')
    async def handle_stop(self, ctx):
        server = self.servers[ctx.guild.id]

        if server.timer == None:
            await ctx.send(
                'Maaf {}, namun sedang tidak ada sesi absen yang berlangsung pada server ini 😥'.format(ctx.author.mention)
            )
        else:
            server = self.servers[ctx.guild.id]

            absentee = server.stop_absen()

            await ctx.send(
                '{}, absen telah selesai! Anda tidak dapat melakukan absen lagi pada sesi ini'.format(server.role.mention)
            )
            await self.write_to_sheet(ctx, absentee)

    async def write_to_sheet(self, ctx, absentee):
        self.sheet.clear_sheet()

        await ctx.send('Kerjaan David')

    """Error handling for handle_init function
    """
    @handle_mulai.error
    @handle_stop.error
    async def handle_errors(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send(
                'Maaf {}, namun anda tidak memiliki hak untuk menjalankan perintah ini 😥'.format(ctx.author.mention)
            )
        else:
            print(error)