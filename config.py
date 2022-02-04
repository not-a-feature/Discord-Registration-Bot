# Config

# Specials Chars like ü/ö should not be used.
# If its needed change the Content-Type of in the MAIL function to utf8

GUILD = 'Grundlagen der Bioinformatik'
STUDENT_ROLE = 'Studierende'
REGEXMAIL = "((\w{1,25})(-\w{1,25})*)\.?(\w{1,25})(-\w{1,25})*@student\.uni-tuebingen\.de"
SMTP_SERVER = "smtpserv.uni-tuebingen.de"
SMTP_PORT = 587  # starttls
SMTP_SENDER = "jules.kreuer@student.uni-tuebingen.de"
SMTP_LOGIN = "zxmog30"

# Path to csv file where the keys will be stored.
CSV_FILE = "registration_keys.csv"

# Prefix of token
TOKEN_PREFIX = "gbi"

# Path to log file
LOGFILE_PATH = "bot.log"


#########
GUILD_APPENDIX = " @ Uni Tuebingen"  # Can be empty
ADMIN_NAME = "Jules"
VERBOSE_EMAIL_REGEX = "first.lastname@student.uni-tuebingen.de"
#########


# Registration email
def MAIL(token):
        return f"""\
From: "{GUILD} Registration Bot" <{SMTP_SENDER}>
Reply-to: {SMTP_SENDER}
Subject: {GUILD} Registration
Content-Type: text/plain

Your registration token is:

{token}

Please copy this token and send it without any addition to the registration-bot.
---

Dein Registrierungstoken lautet:

{token}

Bitte kopiere diesen Token und sende ihn direkt zum Registrierungs-Bot.

~ {GUILD}{GUILD_APPENDIX}
"""


# Welcome message
def WELCOME_MSG(name):
    msg = f"""\
🇬🇧: Hi {name}, welcome to the '{GUILD}'{GUILD_APPENDIX} Discord Server.
Please register with your student email address.
You can do this by sending your email here in the chat.
You will then be sent a token. Please send this token to me (the bot).

Ps: Please change your nick-name to your real name :)

🇩🇪: Hi {name}, willkommen auf dem '{GUILD}'{GUILD_APPENDIX} Discord Server.
Bitte registriere dich mit deiner studentischen Email-Adresse.
Dies kannst du tun indem du deine Email hier in den chat schickst.
Dir wird dann ein Token zugeschickt. Bitte sende Diesen direkt an mich (den Bot).

Ps.: Bitte ändere deinen Nick-Name zu deinem echten Namen :)"""
    return msg

# Help message


HELP_MSG = f"""\
🇬🇧: This bot is used to register students on this Discord server and is intended
to prevent abuse (as far as possible).

To register, the university email must be used. It usually has the following format:

Send your email address without any addition to the bot as a direct message.

You should then have received an email with the subject "{GUILD} Registration".
If not, please check your v-spam folder.

This email contains your (personal) token. This starts with "{TOKEN_PREFIX}".
Copy this token and send it again as a direct message to the bot.
You will then receive the role of "student" and can compose messages and join all channels.

If you have further questions or problems, you can write to the admin ({ADMIN_NAME}).


🇩🇪: Dieser Bot dient zur Registrierung der Studierenden auf diesem Discord-Server und soll
(weitestgehend) Missbrauch verhindern.

Um sich zu registrieren muss die Universitätsemail genutzt werden.
Sie hat in der Regel folgendes Format:
{VERBOSE_EMAIL_REGEX}
Schicke deine Email-Adresse direkt dem Bot als eine Direktnachricht.

Du solltest dann eine Email mit dem Betreff "{GUILD} Registration" erhalten haben.
Falls nicht überprüfe bitte den v-spam Ordner.
Diese Email enthält deinen (persönlichen) Token. Dieser beginnt mit "{TOKEN_PREFIX}".
Kopiere den gesamten Token und schicke ihn dem Bot als Direktnachricht.
Dann erhältst du die Rolle "Studierende" und kannst Nachrichten in allen Kanälen verfassen.

Bei weiteren Fragen und oder Problemen kannst du dem Admin ({ADMIN_NAME}) schreiben.
"""

# Unknown message
UNKNOWN_MESSAGE = """\
🇬🇧: I could not understand your email address / token.
Please send only your email or token into the chat without further ado.
For further help use the command "help" .

🇩🇪: Ich konnte deine Email-Adresse / dein Token nicht verstehen.
Bitte schicke nur deine Email oder dein Token ohne weiteres in den Chat.
Für weitere Hilfe nutzte den Befehl "help" .
"""

# Successfull sending
SUCCESS_SENDING = """\
🇬🇧: An email was sent with the registration token.
🇩🇪: Es wurde eine Email mit dem Registrierungstoken verschickt."""

# Successfull setting role
SUCCESS_SETTING_ROLE = """\
🇬🇧: You have been verified. You will be given student access.
🇩🇪: Du wurdest verifiziert. Du erhällst nun die Rechte eines Studierendens."""

#########

# Error sending email
ERROR_SENDING = """\
🇬🇧: An error accured while sending the email. Please contanct an admin!
🇩🇪: Beim versenden der Email ist etwas schief gelaufen. Bitte kontaktiere einen Admin!"""

# Wrong Token Format (too short / long)
ERROR_TOKEN_FORMAT = """\
🇬🇧: Wrong token format! Please copy the whole token.
🇩🇪: Falsches token format! Botte kopiere den ganzen Token."""

# Token does not belong to sender
ERROR_TOKEN_OWNERSHIP = """\
🇬🇧: This token doesn't belong to you!
🇩🇪: Dieser Token gehört dir nicht!"""

# Token not found
ERROR_TOKEN_NOT_FOUND = """\
🇬🇧: Wrong or unknown token. Please try again or contact an admin.
🇩🇪: Falscher oder unbekante token. Bitte probiere es noch einmal oder kontaktiere an Admin."""

# Error setting role to student
ERROR_SETTING_ROLE = """\
🇬🇧: Could not set role, please try again or contanct an admin.
🇩🇪: Fehler beim Setzen der Rolle. Bitte versuche es noch einmal oder kontaktiere einen Admin."""
