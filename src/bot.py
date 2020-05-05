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
            timer = Timer(time * 60, self.__handle_absen_finished, ctx)

            server.start_absen(timer)

            await ctx.send("{}, sesi absen sedang dimulai.".format(server.role.mention))
            await ctx.send(
                "Segera lakukan absensi dengan mengirimkan pesan `!absentor absen` pada server ini dan tetap _online_ sampai sesi absen selesai."
            )
            await ctx.send("Waktu absen adalah {} menit".format(time))

    """Invoke a command to stop an absen session on a server
    """
    @absentor.command(name='berhenti', aliases=['stop', 'selesai'])
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
            await self.__handle_absen_finished(ctx)

    @absentor.command(name='absen')
    @commands.has_role('@siswa')
    async def handle_absen(self,ctx):
        server = self.servers[ctx.guild.id]

        if server.timer == None:
            await ctx.send(
                "Maaf {}, namun tidak ada sesi absensi yang sedang berjalan 😓".format(ctx.author.mention)
            )
        else:
            if ctx.author.status != Status.online:
                await ctx.send(
                    '{}, anda harus memiliki status Discord _online_ untuk melakukan absensi 😓'.format(ctx.author.mention)
                )
                await ctx.send('Silahkan ubah status Discord anda ke _online_ dan kirimkan ulang perintah anda.')

                return

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
                        "{}, anda telah berhasil diabsen oleh absentor.".format(ctx.author.mention)  
                    )
                    await ctx.send("Mohon untuk tetap _online_ sampai sesi absen selesai")

                    mahasiswa = Mahasiswa(tokens.group(2), tokens.group(1))

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

    """Handler function when absen session is finished
    """
    async def __handle_absen_finished(self, ctx):
        server = self.servers[ctx.guild.id]

        await ctx.send(
            "{}, sesi absen telah selesai! Anda tidak dapat melakukan absen lagi pada sesi ini".format(server.role.mention)
        )

        server.stop_absen()
        self.sheet.clear_absen(date.today())

        absentee = server.absentee
        mahasiswas = []

        for id in absentee:
            member = ctx.guild.get_member(id)

            if member != None and member.status == Status.online:
                mahasiswas.append(absentee[id])

        absentee_str = ""

        for mahasiswa in mahasiswas:
            if len(absentee_str) > 0:
                absentee_str += "\n\r"

            absentee_str += ("**{} <{}>**".format(mahasiswa.name, mahasiswa.npm))

        if len(absentee_str) == 0:
            absentee_str = "Tidak ada yang berhasil melakukan absensi pada sesi absen ini 😥"
        else:
            await ctx.send("Berikut merupakan daftar mahasiswa yang berhasil melakukan absensi:")

        await ctx.send(absentee_str)
        await ctx.send(
            "Catatan: Merubah status menjadi tidak _online_ sebelum sesi absen berakhir mengakibatkan mahasiswa dianggap tidak pernah absen."
        )

        self.sheet.batch_absen(date.today(), mahasiswas)