# Discord-Registration-Bot
This bot was created for the Lecture "Grundlagen der Bioinformatik" in SS 2021 at the University of Tübingen.

## What does this bot do?
This bot is used to register students on a Discord server and is intended to prevent abuse (as far as possible).

To register, the student needs an email that matches a regex. In this case, the university email must be used.
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
- Send a message in this channel welcoming the students and advising them to send their email address to the bot.
- Modify the permissions of the registration channel for `@everyone`:
    - Turn everything off
    - Allow: `Show channel`
    - Allow: `Show message history`

### Discord-API
- Create a Discord-Application at https://discord.com/developers/applications
- Create a Bot with the name `Registration`
- Activate `Server Members Intent`
- Copy the token modify the first line in `tokens.py`
- Go to the OAuth2 Section:
    - Set the scope to `bot`
    - Set the permission to `Manage Roles` and `Send Messages`.
    - Copy the URL and open it. 
- Grant your bot access to your server.

### Discord Part 2
- Go to the Role-Settings
- IMPORTANT: Drag and Drop the roles in the following order:
    - Registration
    - Students
    - @everyone

### Bot
- Modify `config.py` to your needs
    - Set `GUILD` to the name of your server
    - Set `STUDENT_ROLE` to the name of the student's role
    - Set `REGEXMAIL` to a regex of valid / accepted emails
    - Set all `SMTP_` variables accourding to the smtp-server settings
    - Set `CSV_FILE` to the path where the keys will be stored.
    - Set `TOKEN_PREFIX` to a good prefix for the token (Example: "token")
    - Set `GUILD_APPENDIX` to your organisation (Example: Uni Tübingen) 
    - Set `ADMIN_NAME` to the discord name of an admin.
    - Set `VERBOSE_EMAIL_REGEX` to a valid example email.
    - Adapt all strings in the config.py if necessary.

- Set your SMTP email password in the `tokens.py` file
- Install the python `discord` package: `pip install discord`
- Your done :)
### Usage
- Run the python-script
- You may want to create a cron-job that kills the bot every 12 hours and restarts it. This should prevent some bugs and limit downtime.

## Limitations
- This bot will work fine with a small amount (lets say 300) of students. For a more sophisticated bot check out:  https://github.com/jensengillett/verificationbot
- The performance is ok, but not excellent.
- Currently, there is no database connection, the temporary tokens are saved in a csv-file.
- No Brute-Force-Protection
- No Banned email adressed.
- Developed in less than 6 hours --> Shitty Code :)
