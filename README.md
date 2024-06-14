# Pet Profile Management Bot

This Telegram bot helps you create and manage detailed profiles for your pets, including breed, age, size, health issues, allergies, and notes. You can skip any step and come back to it later. The bot also provides periodic reminders to update your pet's details.

## Commands

- `/start`: Initiates the bot and starts the conversation to create or update a pet profile.
- `/set_reminder`: Sets a daily reminder to update your pet's details.
- `/cancel`: Cancels the current conversation.

## Interaction Flow

### Start the Bot

To start the bot, send the `/start` command. The bot will guide you through providing details about your pet.

```text
/start
```

### Provide Pet Details

The bot will ask for the following details. You can skip any step by sending the `/skip` command.

1. **Breed**: What is your pet's breed?
2. **Age**: How old is your pet?
3. **Size**: What is the size of your pet?
4. **Health Issues**: Does your pet have any health issues?
5. **Allergies**: Does your pet have any allergies?
6. **Notes**: Would you like to add any notes about your pet?

### Example Interaction

```text
/start
```

```text
Hi! Let's create a profile for your pet. What is your pet's breed?
```

```text
Indie
```

```text
Great! How old is your pet?
```

```text
3 years
```

```text
What is the size of your pet?
```

```text
Medium
```

```text
Does your pet have any health issues?
```

```text
No
```

```text
Does your pet have any allergies?
```

```text
None
```

```text
Would you like to add any notes about your pet?
```

```text
Very friendly and loves to play fetch.
```

```text
Thank you! Your pet's profile has been created. You can update the details anytime.
```

### Set a Reminder

To set a daily reminder to update your pet's details, send the `/set_reminder` command.

```text
/set_reminder
```

```text
You will be reminded to update your pet's details daily.
```

### Cancel the Conversation

To cancel the current conversation, send the `/cancel` command.

```text
/cancel
```

```text
Bye! I hope we can talk again some day.
```

### Handling Unknown Commands

If you send an unknown command, the bot will inform you and provide guidance on how to use the bot.

```text
/unknowncommand
```

```text
Sorry, I didn't understand that command. Here are the commands you can use:
- /start: Start the conversation to create or update a pet profile.
- /set_reminder: Set a daily reminder to update your pet's details.
- /cancel: Cancel the current conversation.
```

## Running the Bot

Ensure your bot is running by executing the `app.py` script:

```sh
python app.py
```

## Project Structure

```
telegram-bot/
├── app.py
├── conversations.py
├── reminders.py
├── db.py
├── db_schema.sql
├── .env
└── requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory with the following content:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

Replace `your_telegram_bot_token` with your actual Telegram bot token.

## Requirements

Install the required packages using `pip`:

```sh
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License.


sqlite3 pet_bot.db < db_schema.sql