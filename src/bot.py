from threading import Timer
from re import match
from discord import Game, Status
from discord.ext import commands
from datetime import date
from src.model.server import Server
from src.model.mahasiswa import Mahasiswa

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
    @absentor.command(name='mulai', aliases=['start', 'init'])
    @commands.has_role('@botadmin')
    async def handle_mulai(self, ctx, time: int = 15):
        server = self.servers[ctx.guild.id]

        if server.timer != None:
            await ctx.send(
                "Maaf {}, namun telah ada sesi absen yang sedang berlangsung pada server ini 😥".format(ctx.author.mention)
            )
            await ctx.send("Silahkan menunggu sesi absen tersebut selesai.")
            await ctx.send(
                "Anda juga dapat memaksa sesi absen berhenti dengan mengirimkan pesan `!absentor stop`"
            )
        else:
            timer = Timer(time * 60, self.write_to_sheet, ctx)

            server.start_absen(timer)

            await ctx.send("{}, sesi absen sedang dimulai.".format(server.role.mention))
            await ctx.send(
                "Segera lakukan absensi dengan mengirimkan pesan `!absentor absen` pada server ini dan tetap _online_ sampai sesi absen selesai."
            )
            await ctx.send("Waktu absen adalah {} menit".format(time))

    @absentor.command(name='berhenti', aliases=['stop'])
    @commands.has_role('@botadmin')
    async def handle_stop(self, ctx):
        server = self.servers[ctx.guild.id]

        if server.timer == None:
            await ctx.send(
                "Maaf {}, namun sedang tidak ada sesi absen yang sedang berlangsung pada server ini 😥"
                .format(ctx.author.mention)
            )
            await ctx.send(
                "Anda dapat memulai sesi absen dengan mengirimkan pesan `!absentor mulai`"
            )
        else:
            server = self.servers[ctx.guild.id]

            absentee = server.stop_absen()

            await ctx.send(
                '{}, absen telah selesai! Anda tidak dapat melakukan absen lagi pada sesi ini'.format(server.role.mention)
            )
            await self.write_to_sheet(ctx, absentee)

    async def write_to_sheet(self, ctx, absentee):
        self.sheet.clear_absen(date.today())

        await ctx.send('Kerjaan David')

    @absentor.command(name='absen')
    @commands.has_role('@siswa')
    async def handle_absen(self,ctx):
        server = self.servers[ctx.guild.id]

        if server.timer == None:
            await ctx.send(
                "Maaf {}, namun tidak ada sesi absensi yang sedang berjalan 😓".format(ctx.author.mention)
            )
        else:
            fullname = ctx.author.nick

            if fullname == None:
                fullname = ctx.author.name

            id = ctx.author.id

            if server.has_absentee(id):
                await ctx.send(
                    "{}, anda sudah terabsen sebelumnya. Anda tidak perlu absen lebih dari sekali karena absentor tidak mungkin lupa 😉.".format(ctx.author.mention)
                )
            else:
                tokens = match(r"(\w+) - (\d{10})", fullname)

                if tokens == None:
                    await ctx.send(
                        "Maaf {}, namun format nama anda tidak sesuai.".format(ctx.author.mention)
                    )
                    await ctx.send("Tolong rubah nama anda menjadi `<nama> - <npm>`")
                    await ctx.send("PS: Anda dapat memiliki nama khusus untuk server ini saja 😉")
                else:
                    await ctx.send(
                        "{}, anda sudah diabsen oleh absentor.".format(ctx.author.mention)  
                    )
                    await ctx.send("Mohon untuk tetap _online_ sampai sesi absen selesai")

                    mahasiswa = Mahasiswa(tokens.group(1), tokens.group(2))

                    server.add_absentee(id, mahasiswa)

    """Error handling for all handler function
    """
    @handle_mulai.error
    @handle_stop.error
    async def handle_errors(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send(
                "Maaf {}, namun anda tidak memiliki hak untuk menjalankan perintah ini 😥".format(ctx.author.mention)
            )
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(
                "Maaf {}, namun absentor tidak mengerti maksud permintaan anda 😥".format(ctx.author.mention)
            )
        else:
            print(error)

    async def handle_mahasiswa_offline(self,server_id):
        server = self.servers[server_id]
        guild = self.bot.get_guild(server_id)
        channel = self.bot.get_channel(695181326793310269)
        siswa_id_offline = []
        result = ""
        for siswa_id in server.get_absentee().keys():
            member = guild.get_member(siswa_id)
            if member.status == Status.offline:
                result += '{}'.format(member.mention)
                siswa_id_offline.append(siswa_id)

        for siswa_id in siswa_id_offline:
            server.delete_entry(siswa_id)

        if result != "":
            result += "\n anda tidak diabsen karena anda offline sebelum durasi berakhir"
            await channel.send(result)