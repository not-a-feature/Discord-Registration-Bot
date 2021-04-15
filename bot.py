import discord
from discord.utils import get
from os.path import isfile
from re import fullmatch as regmatch
from secrets import token_hex
import smtplib, ssl
from sys import exit
import logging

from tokens import TOKEN, SMTP_PASSWORD

'''
Discord-Registration-Bot by Jules Kreuer / not-a-feature
See: https://github.com/not-a-feature/Discord-Registration-Bot
License: GPL-3.0
'''

GUILD = 'TestserverGBI'
STUDENT_ROLE = 'Studierende'
REGEXMAIL = "((\w{1,25})(-\w{1,25})?)\.(\w{1,25})(-\w{1,25})?@student\.uni-tuebingen\.de"
SMTP_SERVER = "smtpserv.uni-tuebingen.de"
SMTP_PORT = 587  # starttls
SMTP_SENDER = "jules.kreuer@student.uni-tuebingen.de"
SMTP_LOGIN = "zxmog30"
CSV_FILE = "registration_keys.csv"

logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class RegistrationClient(discord.Client):
    async def on_ready(self):

        if not isfile(CSV_FILE):
            logging.info("No Registration-Token file found! Creating a new (empty) one.")
            try:
                open(CSV_FILE, "a").close()
            except:
                logging.error("Can't write to Token-File")
                exit()
        
        guild = discord.utils.get(self.guilds, name=GUILD)    
        logging.info(f'{self.user} has connected to Discord!')
        logging.info(f'{guild.name}(id: {guild.id})')

        await self.change_presence(status=discord.Status.online, activity=discord.Game("Schreibe mich an!"))
        print("BOT IS RUNNING!")
    
    # Automatic message when a user joins the chat
    # Does not work? Still don't know why
    '''
    async def on_member_join(self, member):
        logging.info(f"{member.name} joined the server")
        await member.create_dm()
        await member.dm_channel.send(f"""
🇬🇧: Hi {member.name}, welcome to the 'Grundlagen der Bioinformatik' @ Uni Tübingen Discord Server.
Please register with your student email address.
You can do this by sending your email here in the chat.
You will then be sent a token.

🇩🇪: Hi {member.name}, willkommen auf dem 'Grundlagen der Bioinformatik' @ Uni Tübingen Discord Server.
Bitte registriere dich mit deiner studentischen Email-Adresse.
Dies kannst du tun indem du deine Email hier in den chat schickst. 
Dir wird dann ein Token zugeschickt.
""")
    '''

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        cnl  = message.channel
        cont = message.content.lower().strip()
        logging.info(f'New Message from {message.author}: {cont}')

        if cont in ['!stats', '!ping']:
            await cnl.send(f"pong with {str(round(self.latency, 2))} ms latency")
            await cnl.send(f"{str(len(open(CSV_FILE).readlines()))} pending registrations")
            return
        
        if regmatch(REGEXMAIL, cont):
            logging.info(f'New Email: {cont}')
            token = "gbi-" + str(message.author.id) + "-" + str(token_hex(16))[:16]
            await self.saveToken(cont, token)
            await self.sendMail(message, cont, token)
            return

        if cont.startswith("gbi-"):
            await self.verify(message, cont)
            return

        if cont in ["!help", "help", '"help"' "!hilfe", "hilfe", '"hilfe"']:
            await cnl.send("""
🇬🇧: This bot is used to register students on this Discord server and is intended to prevent abuse (as far as possible).

To register, the university email must be used. It usually has the following format: first.lastname@student.uni-tuebingen.de
Send your email address directly to the bot as a direct message.

You should then have received an email with the subject "GBi Registration".If not, please check your v-spam folder.
This email contains your (personal) token. This starts with "gbi-".
Copy this token and send it again as a direct message to the bot.
You will then receive the role of "student" and can compose messages and join all channels.

If you have further questions or problems, you can write to the admin (Jules).


🇩🇪: Dieser Bot dient zur Registrierung der Studierenden auf diesem Discord-Server und soll (weitestgehend) Missbrauch verhindern.

Um sich zu registrieren muss die Universitätsemail genutzt werden. Sie hat in der Regel folgendes Format: vorname.nachname@student.uni-tuebingen.de
Schicke deine Email-Adresse direkt dem Bot als eine Direktnachricht.

Du solltest dann eine Email mit dem Betreff "GBi Registration" erhalten haben. Falls nicht überprüfe bitte den v-spam Ordner.
Diese Email enthält deinen (persönlichen) Token. Dieser beginnt mit "gbi-".
Kopiere diesen Token und schicke ihn wieder als Direktnachricht dem Bot.
Dann erhältst du die Rolle "Studierende" und kannst Nachrichten verfassen und allen Kanälen beitreten.

Bei weiteren Fragen und oder Problemen kannst du dem Admin (Jules) schreiben.
""")
            return

        await cnl.send("""
🇬🇧: I could not understand your email address / token.
Please send only your email or token into the chat without further ado.
For further help use the command "help" .

🇩🇪: Ich konnte deine Email-Adresse / dein Token nicht verstehen.
Bitte schicke nur deine Email oder dein Token ohne weiteres in den Chat.
Für weitere Hilfe nutzte den Befehl "help" .
""")


    async def sendMail(self, message, adress, token):
        cnl  = message.channel

        body = f"""\
From: "GBi Registration Bot" <{SMTP_SENDER}>
Reply-to: {SMTP_SENDER}
Subject: GBi Registration
Content-Type: text/plain

Your registration token is:

{token}

Please copy this token and send it without any addition to the registration-bot.
---

Dein Registrierungstoken lautet:

{token}

Bitte kopiere diesen Token und sende ihn direkt zum Registrierungs-Bot.

~The GBi Team
"""

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        logging.debug(f'Start sending Email to {adress}')
        try:
            server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
            server.ehlo() # Can be omitted
            server.starttls(context=context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(SMTP_LOGIN, SMTP_PASSWORD)
            logging.debug(f'SMTP login successfull')
            server.sendmail(SMTP_SENDER, adress, body)
            logging.debug(f'End sending Email')
            
        except Exception as e:
            logging.error(f'Could not send email to {adress} with token {token}')
            await cnl.send("An error accured while sending the email. Please contanct an admin / Beim versenden der Email ist etwas schief gelaufen. Bitte kontaktiere einen Admin")
            return
        finally:
            server.quit() 
        await cnl.send("An email was sent with the registration token. / Es wurde eine Email mit dem Registrierungstoken verschickt.")
        
    
    async def saveToken(self, adress, token):
        # Delete old Token
        shortToken = token[:-16]
        longToken = token + ";" + adress
        newFileContent = []
        try:
            logging.debug(f'Start saving token: {longToken}')
            for line in open(CSV_FILE, "r"):
                if not line.startswith(shortToken):
                    newFileContent.append(line)
            
            # Write new Token
            newFileContent.append(longToken)
            with open(CSV_FILE, "w") as f:
                f.writelines(newFileContent)
            logging.info(f'Token was saved: {longToken}')
        except Exception as e:
            logging.warning(f'Could not save token {longToken}. Error: {e}')


    async def verify(self, message, cont):
        cnl  = message.channel

        if not cont[4:][:-17] == str(message.author.id):
            logging.warning(f'Wrong user-id! May be a hacking attempt: {cont} from {message.author.id}')
            await cnl.send("This token doesn't belong to you! / Dieser Token gehört dir nicht!")
            return
        newFileContent = []
        tokenFound = False
        try:
            logging.debug(f'Start searching for token: {cont}')
            for line in open(CSV_FILE, "r"):
                if line.startswith(cont):
                    tokenFound = True
                    logging.debug(f'Token found.')
                else:
                    newFileContent.append(line)
        except Exception as e:
            logging.warning(f'Could read token file. Error: {e}')

        if not tokenFound:
            logging.warning(f'Token not found.')
            await cnl.send("Wrong or unknown token. Please try again or contact an Admin / Falscher oder unbekante token. Bitte probiere es noch einmal oder kontaktiere an Admin")
            return
        # Correct Token
        try:
            with open(CSV_FILE, "w") as f:
                f.writelines(newFileContent)
        except Exception as e:
            logging.warning(f'Could write token file. Error: {e}')
        try:
            guild = discord.utils.get(self.guilds, name=GUILD)      
            member = await guild.fetch_member(int(message.author.id))
            role = get(member.guild.roles, name=STUDENT_ROLE)
            await member.add_roles(role)
            logging.info(f'{member} got the role: {role}')

        except Exception as e:
            logging.error(f'Could set user role: {e}')
            await cnl.send("Could not set role, please try again or contanct an admin / Fehler beim Setzen der Rolle. Bitte versuche es noch einmal oder kontaktiere einen Admin.")
            return
        await cnl.send("You have been verified. You will be given student access. / Du wurdest verifiziert. Du erhällst nun die Rechte eines Studierendens")

bot = RegistrationClient()
bot.run(TOKEN)
