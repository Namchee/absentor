from google.oauth2.service_account import Credentials
from discord.ext.commands import Bot
from discord import Game, Status
from os import environ
from dotenv import load_dotenv, find_dotenv
from gspread import authorize
from datetime import date
from src.model.bot import AbsentorBot
from src.model.sheet import Sheet
from src.model.mahasiswa import Mahasiswa

load_dotenv(find_dotenv())

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file('credentials.json', scopes=scope)

gc = authorize(credentials)
spreadsheet = gc.open_by_key(environ.get("SHEET_ID"))

sheet = Sheet(spreadsheet, spreadsheet.get_worksheet(0))

bot = Bot(command_prefix="!")
bot.add_cog(AbsentorBot(bot, sheet))

"""On connection, log all guilds connected to this bot instance
    And change the status
"""
@bot.event
async def on_ready():
    print('Absentor is connected to these servers:')

    for guild in bot.guilds:
        print('{} ({})'.format(guild.name, guild.id))

    await bot.change_presence(status=Status.online, activity=Game(name="Absensi Mahasiswa"))

def main():
    mahasiswa1 = Mahasiswa("2017730017", "Cristopher")
    mahasiswa2 = Mahasiswa("2017730015", "David Christoper Sentosa")

    sheet.batch_absen(date.today(), [mahasiswa1, mahasiswa2])

if __name__ == "__main__":
    main()