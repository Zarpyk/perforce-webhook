# Perforce Commit Discord Webhook
**Scripts modified from: https://github.com/JamesIves/perforce-commit-discord-bot**

Modifications:
- Fix commit messages having empty lines
- Change message format to `> Message`
- Add timestamp
- Fix repeat commit message when restart bot
- Fix repeat commit message when perforce down/restarting
- Change color to green
- Replace Enviroment key with webhook link (**You need change the link on app.py**)
- Add debug message on console
- Add start script (**You need init python venv and install requirements to use the script** `python -m venv /path/to/this-project`)
- Remove tests

![image](https://user-images.githubusercontent.com/30746531/230206250-8f5b62a8-302e-41a5-868e-0bfccc8f11a3.png)

-------------------------------------------------

# Perforce Commit Logger Discord Bot 🗒️ ✏️

With this bot you're able to keep track of commits made to a [Perforce version control](https://www.perforce.com/) server within a [Discord](https://discordapp.com/) channel. 

## Installation Steps 💽

1. Within your Discord server go to the settings for the channel you'd like the commit logs to be posted to and copy the webhook URL.
2. Save the webhook URL as an environment variable called `DISCORD_WEBHOOK_URL`. 
3. The service requires access to the `p4 changes` command in the terminal, your bot should be installed somewhere where it can automatically perform this command without the session expiring. Once suitable access has been provided you'll need to run `$ pip install -r requirements.txt` followed by `$ python app.py` to initialize it.
4. Optionally you should consider creating a CRON script or something similar that restarts the `app.py` file on server reboot in order to keep the bot alive.

---

Unit tests can be run using the `$ python tests.py` command.

## Getting Started :airplane:

Every thirty seconds the bot runs a Perforce command in the terminal that checks for the most recent changes. If it finds one it stores it in memory, if the change it finds is the same as the one it gathered previously then it discards it. You'll need to provide the bot with access to your servers Perforce command line. One way of doing this is running the Python application on the server which hosts your Perforce instance. If you can type `p4 changes` yourself then the bot will be able to do its thing.

## Configuration 📁

The installation will require you to enter a number of settings as environment variables. Below you'll find an explanation of each.

| Key  | Value Information | Required |
| ------------- | ------------- | ------------- |
| `DISCORD_WEBHOOK_URL`  | The [Webhook URL](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for the Discord channel you'd like the bot to post its messages to. | **Yes** |
