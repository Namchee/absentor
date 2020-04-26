from google.oauth2.service_account import Credentials
from discord.ext.commands import Bot
from os import environ
from dotenv import load_dotenv, find_dotenv
from gspread import authorize
from datetime import date
from src.bot import AbsentorBot
from src.sheet import Sheet
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

def main():
    pass

if __name__ == "__main__":
    main()