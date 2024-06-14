from telegram import Bot
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
# Initialize your Telegram Bot with the bot token

if __name__ == '__main__':    
    bot = Bot(token=telegram_token)
        # List of recipient chat IDs
    recipients = [1109512003]

    # Broadcast message content
    broadcast_message = "This is a broadcast message."

    # Send the broadcast message to all recipients
    async def send_broadcast_message():
        for chat_id in recipients:
            await bot.send_message(chat_id=chat_id, text=broadcast_message)
            # await bot.send_photo(chat_id=chat_id, photo='https://makemyai.in/assets/MakemyAI-eXvCuAsa.gif')

    # Run the event loop to send the broadcast message
    asyncio.run(send_broadcast_message())