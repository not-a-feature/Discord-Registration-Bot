# Discord-Registration-Bot
This bot was created for the Lecture "Grundlagen der Bioinformatik" in SS 2021 at the University of Tübingen.

## What does this bot do?
This bot is used to register students on a Discord server and is intended to prevent abuse (as far as possible).

To register, the student needs an email that matches a regex. In this case the university email must be used.
The student must send their email address to the bot as a direct message.

Then they should get an email with a (random) token.

This token should be copied and send again as a direct message to the bot.
The student will then receive the role of "student" and can compose messages and join all channels.

## Setup
### Discord
- Create a Discord-server
- Create a Role for the students
- Remove all permissions of the role `@everyone`
- Create a channel called registration
- Send an message in this channel welcoming the students and advising them to send their email-adress to the bot.
- Modify the permissions of the registration channel for `@everyone`:
    - Turn everything off
    - Allow: `Show channel`
    - Allow: `Show message history`

### Discord-API
- Create an Discord-Application at: https://discord.com/developers/applications
- Create a Bot with the name `Registration`
- Copy the Token and Save modify the first line in `tokens.py`
- Go to the OAuth2 Section:
    - Set the scope to `bot`
    - Set the permission to `Manage Roles` and `Send Messages` (maybe only manage roles will work too)
    - Copy the url and open it. 
- Grant your bot acces to your server.

### Discord Part 2
- Go to the Role-Settings
- IMPORTANT: Drag and Drop the roles to following order:
    - Registration
    - Students
    - @everyone

### Bot
- Modify the text to your needs
- Set `GUILD` to the name of your server
- Set `STUDENT_ROLE` to the name of the students role
- Set `REGEXMAIL` to a regex of valid / accepted emails
- Set your SMTP credentials (password is in the `tokens.py` file) 
- Install the python `discord` package: `pip install discord`
- Run the python-script
- You may want to create a cron-job that kills the bot every 6 hours and restart it. This should prevent some bugs and limit the downtime.

## Limitations
- This bot will only work with a small amount (< 200) of students. For a more sophisticated bot check out:  https://github.com/jensengillett/verificationbot
- The performance is ok, but not great.
- Currently there is no database-connection, the temporary tokens are saved in a csv-file.
- No Brute-Force-Protection
- Developed in less than 6 hours --> Shitty Code

