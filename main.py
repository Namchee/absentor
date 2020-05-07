from google.oauth2.service_account import Credentials
from discord.ext.commands import Bot
from os import environ
from dotenv import load_dotenv, find_dotenv
from gspread import authorize
from src.bot import AbsentorBot
from src.sheet import Sheet

load_dotenv(find_dotenv())

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials_info = {
    'type': environ.get('TYPE'),
    'project_id': environ.get('PROJECT_ID'),
    'private_key_id': environ.get('PRIVATE_KEY_ID'),
    'private_key': environ.get('PRIVATE_KEY'),
    'client_email': environ.get('CLIENT_EMAIL'),
    'client_id': environ.get('CLIENT_ID'),
    'auth_uri': environ.get('AUTH_URI'),
    'token_uri': environ.get('TOKEN_URI'),
    'auth_provider_x509_cert_url': environ.get('AUTH_PROVIDER_X509_CERT_URL'),
    'client_x509_cert_url': environ.get('CLIENT_X509_CERT_URL')
}

credentials = Credentials.from_service_account_info(credentials_info, scopes=scope)

gc = authorize(credentials)
spreadsheet = gc.open_by_key(environ.get("SHEET_ID"))

sheet = Sheet(spreadsheet, spreadsheet.get_worksheet(0))

bot = Bot(command_prefix="!")
bot.add_cog(AbsentorBot(bot, sheet))

def main():
    bot.run(environ.get("DISCORD_TOKEN"))

if __name__ == "__main__":
    main()