# TruckersMP Version Tracker

**TruckersMP Version Tracker** is a Discord bot that tracks the supported versions of TruckersMP for Euro Truck Simulator 2 and American Truck Simulator, notifying your server of any updates.

## Commands

### Admin Commands

- **/manage_channel** - Change the notification channel for version updates.
- **/set_games** - Specify which games to monitor (ETS2 or ATS).
- **/set_role** - Set the role to be notified of updates.
- **/set_frequency** - Adjust the delay between version checks.
- **/toggle** - Enable or disable version tracking.
- **/info** - Display current tracker settings and status.

### General Commands

- **/tmp_version** - Show the latest supported versions of ETS2 and ATS.

## Setup Instructions

### 1. Create Your Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click "New Application" and give your bot a name.
3. In the left sidebar, go to the "Bot" tab and click "Add Bot."
4. Once the bot is created, under the "Token" section, click "Copy" to save your bot token (you'll need this in the next step).
5. Under "Privileged Gateway Intents," enable the **MESSAGE INTENT** and **SERVER MEMBERS INTENT** options.

### 2. Add the Bot to Your Server

1. In the Discord Developer Portal, go to the "OAuth2" tab and select "URL Generator."
2. Under "Scopes," select **bot**.
3. Under "Bot Permissions," select the necessary permissions (typically **Administrator** if you want full control).
4. Copy the generated link at the bottom and paste it into your browser.
5. Select your server and click "Authorize" to add the bot.

### 3. Configure the Bot in the Code

1. Download or clone the code from this repository.
2. Open the bot's code in any text editor (e.g., VSCode, PyCharm).
3. At the bottom of the code, you need to paste your token. Look for this line:

    ```python
    bot.run('YOUR_BOT_TOKEN')
    ```

4. Replace `'YOUR_BOT_TOKEN'` with the token you copied earlier from the Discord Developer Portal:

    ```python
    bot.run('YOUR_ACTUAL_BOT_TOKEN')
    ```

5. Save the changes.

### 4. Run Your Bot

1. Make sure you have [Python](https://www.python.org/downloads/) installed.
2. Start the bot by running the Python file.

Your bot should now be running and available on your server!

### 5. Optional: Add My Bot Instead

If you don't want to create your own bot, you can add my pre-configured bot to your server. Just click on the link below:

[Add my bot](https://discord.com/oauth2/authorize?client_id=1291060777947496509)


## Credits

Developed by **bdvzk**. Contributions are welcome!
