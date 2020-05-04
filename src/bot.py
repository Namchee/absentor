from discord import Game, Status
from discord.ext import commands
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

    """Invoka a command to initiate an absen session.
        Will fail if the invoker is not the guild owner or doesn't have @botadmin role.
        Parameters:
            - time {int}: Time limit for an absen session
    """
    @absentor.command(name='mulai')
    @commands.has_role('@botadmin')
    async def handle_init(self, ctx, time: int = 15):
        server = self.servers[ctx.guild.id]

        if server.is_absen:
            await ctx.send(
                'Maaf {}, namun telah ada sesi absen yang sedang berlangsung pada server ini. 🤔'.format(ctx.author.mention)
            )
            await ctx.send('Silahkan menunggu sesi absen tersebut selesai.')

            return
        else:
            role = server.role

            server.start_absen()
            await ctx.send(
                '{}, sesi absen sedang dimulai. Segera lakukan absensi dengan mengirimkan pesan `!absentor absen` pada server ini dan tetap _online_ sampai sesi absen selesai.'.format(role.mention)
            )
            await ctx.send('Waktu absen = {} menit'.format(time))

    """Error handling for handle_init function
    """
    @handle_init.error
    async def handle_init_absen_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send(
                'Maaf {}, namun anda tidak memiliki hak untuk menjalankan perintah ini 😥'.format(ctx.author.mention)
            )
        else:
            print(error)

    @absentor.command(name='absen')
    @commands.has_role('@siswa')
    async def handle_mahasiswa_absen(self,ctx):
        server = self.servers[ctx.guild.id]
        if not server.is_absen:
            await ctx.send(
                "Maaf {}, absensi sedang tidak dimulai".format(ctx.author.mention)
            )
        else:
            fullname = ctx.author.nick
            id = ctx.author.id
            if server.already_absent(id):
                await ctx.send('{}, anda sudah absen'.format(ctx.author.mention))
            else:
                nama,npm = fullname.split("-")
                await ctx.send('{}, anda sudah absen jangan pergi sebelum durasi selesai'.format(ctx.author.mention))
                server.add_absentee(id, Mahasiswa(npm, nama))


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