import logging
import os
import sys
from telegram import Bot
from telegram.ext import Application, ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

from conversations import get_conversation_handler
from commands import help_command, unknown

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(telegram_token).build()

    # Store OpenAI API key in bot_data for access in handlers
    # application.bot_data['openai_api_key'] = openai_api_key

    # Add conversation handler with the states USER_DETAILS and PET_DETAILS
    application.add_handler(get_conversation_handler())
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == '__main__':    
    main()
