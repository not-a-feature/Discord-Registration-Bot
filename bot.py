import discord
from discord.utils import get
from os.path import isfile
from re import fullmatch as regmatch
from secrets import token_hex
import smtplib, ssl
from sys import exit
import logging

# Import smtp password and other config
from tokens import TOKEN, SMTP_PASSWORD
from config import *

"""
Discord-Registration-Bot by Jules Kreuer / not-a-feature
See: https://github.com/not-a-feature/Discord-Registration-Bot
License: GPL-3.0
"""
print(f"{GUILD} Discord Bot")


logging.basicConfig(
    filename=LOGFILE_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

intents = discord.Intents.default()
intents.members = True


class RegistrationClient(discord.Client):
    async def on_ready(self):
        # Check / Create new token file
        if not isfile(CSV_FILE):
            logging.info("No Registration-Token file found! Creating a new (empty) one.")
            try:
                open(CSV_FILE, "a").close()
            except:
                logging.error("Can't write to Token-File")
                exit()

        guild = discord.utils.get(self.guilds, name=GUILD)
        logging.info(f"{self.user} has connected to Discord!")
        logging.info(f"{guild.name}(id: {guild.id})")

        await self.change_presence(status=discord.Status.online, activity=discord.Game("Write me!"))
        print("BOT IS RUNNING!")

    # Automatic message when a user joins the chat
    async def on_member_join(self, member):
        logging.info(f"{member.name} joined the server")
        await member.create_dm()
        await member.dm_channel.send(WELCOME_MSG(member.name))

    # Answer on messages
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        cnl = message.channel
        cont = message.content.lower().strip()
        logging.info(f"New Message from {message.author}: {cont}")

        # Case: Message matches email pattern.
        if regmatch(REGEXMAIL, cont):
            logging.info(f"New Email: {cont}")
            # Create token: Prefix + "-" + User ID + Random
            token = f"{TOKEN_PREFIX}-{message.author.id}-{token_hex(16)[:16]}"
            await self.saveToken(cont, token)
            await self.sendMail(message, cont, token)
            return

        # Case: Message starts with token prefix.
        elif cont.startswith(TOKEN_PREFIX):
            await self.verify(message, cont)
            return

        # Case: Help command.
        elif cont in ["!help", "help", '"help"' "!hilfe", "hilfe", '"hilfe"']:
            await cnl.send(HELP_MSG)
            return

        # Case: Statistics command.
        elif cont in ["!stats", "!ping"]:
            await cnl.send(f"pong with {str(round(self.latency, 3))} s latency")
            await cnl.send(f"{str(len(open(CSV_FILE).readlines()))} pending registrations")
            return

        await cnl.send(UNKNOWN_MESSAGE)

    async def sendMail(self, message, adress, token):
        cnl = message.channel

        body = MAIL(token)

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        logging.debug(f"Start sending Email to {adress}")
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(SMTP_LOGIN, SMTP_PASSWORD)
            logging.debug(f"SMTP login successfull")
            server.sendmail(SMTP_SENDER, adress, body)
            logging.debug(f"End sending Email")

        except Exception as e:
            logging.error(f"Could not send email to {adress} with token {token}. Error: {e}")
            await cnl.send(ERROR_SENDING)
            return
        finally:
            server.quit()
        await cnl.send(SUCCESS_SENDING)

    async def saveToken(self, adress, token):
        # Delete old Token
        shortToken = token[:-16]
        longToken = token + ";" + adress
        newFileContent = []
        try:
            logging.debug(f"Start saving token: {longToken}")
            for line in open(CSV_FILE, "r"):
                if not line.startswith(shortToken):
                    newFileContent.append(line)

            # Write new Token
            newFileContent.append(longToken + "\n")
            with open(CSV_FILE, "w") as f:
                f.writelines(newFileContent)
            logging.info(f"Token was saved: {longToken}")
        except Exception as e:
            logging.warning(f"Could not save token {longToken}. Error: {e}")

    async def verify(self, message, cont):
        cnl = message.channel
        contArr = cont.split("-")
        # Token should consists of 3 parts
        if not len(contArr) == 3:
            logging.warning(f"Wrong token format! {cont} from {message.author.id}")
            await cnl.send(ERROR_TOKEN_FORMAT)
            return

        # UID of token-request should match with uid of token-sender.
        if not contArr[1] == str(message.author.id):
            logging.warning(f"Wrong user-id {cont} from {message.author.id}")
            await cnl.send(ERROR_TOKEN_OWNERSHIP)
            return

        # Search for tokens in file
        newFileContent = []
        tokenFound = False
        try:
            for line in open(CSV_FILE, "r"):
                if cont == line.split(";", 1)[0]:
                    tokenFound = True
                    logging.debug(f"Token found.")
                else:
                    newFileContent.append(line)

        except Exception as e:
            logging.warning(f"Could read token file. Error: {e}")

        if not tokenFound:
            logging.warning(f"Token not found.")
            await cnl.send(ERROR_TOKEN_NOT_FOUND)
            return

        # Correct Token
        try:
            # Write file without used token
            with open(CSV_FILE, "w") as f:
                f.writelines(newFileContent)
        except Exception as e:
            logging.warning(f"Could write token file. Error: {e}")

        try:
            # Set role to student
            guild = discord.utils.get(self.guilds, name=GUILD)
            member = await guild.fetch_member(int(message.author.id))
            role = get(member.guild.roles, name=STUDENT_ROLE)
            await member.add_roles(role)
            logging.info(f"{member} got the role: {role}")

        except Exception as e:
            logging.error(f"Could not set user role. Error: {e}")
            await cnl.send(ERROR_SETTING_ROLE)
            return
        await cnl.send(SUCCESS_SETTING_ROLE)


bot = RegistrationClient(intents=intents)
bot.run(TOKEN)
