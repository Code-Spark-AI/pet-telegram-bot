from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "Here are the commands you can use:\n"
        "- /start: Start the conversation to create or update a pet profile.\n"
        "- /cancel: Cancel the current conversation."
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    await update.message.reply_text(
        "Sorry, I didn't understand that command. Here are the commands you can use:\n"
        "- /start: Start the conversation to create or update a pet profile.\n"
        "- /cancel: Cancel the current conversation."
    )
