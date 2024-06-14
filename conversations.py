from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import logging
from reminders import set_reminder, set_playtime_reminder
from croniter import croniter
from datetime import datetime
from db import get_db_connection  # Import the function from db.py

import re
from datetime import datetime


# Define states
PET_NAME, BREED, AGE, SIZE, HEALTH_ISSUES, ALLERGIES, NOTES, WEIGHT, MEASUREMENTS, PLAYTIME = range(10)

# Define reply keyboards
breed_keyboard = [['Indie'], ['Labrador'], ['Poodle'], ['Bulldog'], ['Others']]
age_keyboard = [['Less than 3 months'], ['Less than 6 months'], ['Less than 1 year'], ['1-2'], ['3-5'], ['6-8'], ['Greater than 8']]
size_keyboard = [['Small'], ['Medium'], ['Large']]
yes_no_keyboard = [['Yes'], ['No']]
markup_breed = ReplyKeyboardMarkup(breed_keyboard, one_time_keyboard=True)
markup_age = ReplyKeyboardMarkup(age_keyboard, one_time_keyboard=True)
markup_size = ReplyKeyboardMarkup(size_keyboard, one_time_keyboard=True)
markup_yes_no = ReplyKeyboardMarkup(yes_no_keyboard, one_time_keyboard=True)

# Initialize logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Hi! Let's create a profile for your pet. What is your pet's name?",
        reply_markup=ReplyKeyboardRemove(),
    )
    context.user_data['current_state'] = PET_NAME
    return PET_NAME

async def pet_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    pet_name = update.message.text
    context.user_data['pet_name'] = pet_name
    context.bot_data[user.id] = context.user_data
    logger.info("Pet's name provided by %s: %s", user.first_name, pet_name)
    await update.message.reply_text(
        "Great! What is your pet's breed?",
        reply_markup=markup_breed,
    )
    context.user_data['current_state'] = BREED
    return BREED

async def breed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    breed = update.message.text
    if breed == 'Others':
        await update.message.reply_text("Please type your pet's breed.")
        return BREED
    context.user_data['breed'] = breed
    context.bot_data[user.id] = context.user_data
    logger.info("Breed of %s's pet: %s", user.first_name, breed)
    await update.message.reply_text(
        "Great! How old is your pet?",
        reply_markup=markup_age,
    )
    context.user_data['current_state'] = AGE
    return AGE

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    age = update.message.text
    if age == 'Others':
        await update.message.reply_text("Please type your pet's age.")
        return AGE
    context.user_data['age'] = age
    context.bot_data[user.id] = context.user_data
    logger.info("Age of %s's pet: %s", user.first_name, age)
    await update.message.reply_text(
        "What is the size of your pet?",
        reply_markup=markup_size,
    )
    context.user_data['current_state'] = SIZE
    return SIZE

async def size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    size = update.message.text
    if size == 'Others':
        await update.message.reply_text("Please type your pet's size.")
        return SIZE
    context.user_data['size'] = size
    context.bot_data[user.id] = context.user_data
    logger.info("Size of %s's pet: %s", user.first_name, size)
#     await update.message.reply_text(
#         "Does your pet have any health issues?",
#         reply_markup=markup_yes_no,
#     )
#     context.user_data['current_state'] = HEALTH_ISSUES
#     return HEALTH_ISSUES

# async def health_issues(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     user = update.message.from_user
#     health_issues = update.message.text
#     context.user_data['health_issues'] = health_issues
#     context.bot_data[user.id] = context.user_data
#     logger.info("Health issues of %s's pet: %s", user.first_name, health_issues)
#     await update.message.reply_text(
#         "Does your pet have any allergies?",
#         reply_markup=markup_yes_no,
#     )
#     context.user_data['current_state'] = ALLERGIES
#     return ALLERGIES

# async def allergies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     user = update.message.from_user
#     allergies = update.message.text
#     context.user_data['allergies'] = allergies
#     context.bot_data[user.id] = context.user_data
#     logger.info("Allergies of %s's pet: %s", user.first_name, allergies)
#     await update.message.reply_text(
#         "Would you like to add any notes about your pet?",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     context.user_data['current_state'] = NOTES
#     return NOTES

# async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     user = update.message.from_user
#     context.user_data['notes'] = update.message.text
#     context.bot_data[user.id] = context.user_data
#     logger.info("Notes for %s's pet: %s", user.first_name, update.message.text)
    
    await update.message.reply_text(
        "Please provide your pet's weight (in Kgs).",
        reply_markup=ReplyKeyboardRemove(),
    )
    context.user_data['current_state'] = WEIGHT
    return WEIGHT

async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_data = context.user_data
    context.user_data['weight'] = update.message.text
    context.bot_data[user.id] = user_data
    logger.info("Weight of %s's pet: %s", user.first_name, update.message.text)
#     await update.message.reply_text(
#         "Please provide any other measurements for your pet (e.g. height, length).",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     context.user_data['current_state'] = MEASUREMENTS
#     return MEASUREMENTS

# async def measurements(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     user = update.message.from_user
#     context.user_data['measurements'] = update.message.text
#     context.bot_data[user.id] = context.user_data
#     logger.info("Measurements for %s's pet: %s", user.first_name, update.message.text)

#     context.user_data['current_state'] = PLAYTIME
#     return PLAYTIME

# async def playtime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     user = update.message.from_user
#     user_data = context.user_data
#     context.bot_data[user.id] = context.user_data
    
    
    #Save pet details to the database
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO pets (user_id, pet_name, breed, pet_age, size, health_issues, allergies, notes, weight, measurements) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (user.id, user_data.get('pet_name'), user_data.get('breed'), user_data.get('age'), user_data.get('size'), user_data.get('health_issues'), user_data.get('allergies'), user_data.get('notes'), user_data.get('weight'), user_data.get('measurements'))
    )
    
    # Check if the user ID already exists
    existing_user = conn.execute('SELECT user_id FROM users WHERE user_id = ?', (user.id,)).fetchone()

    if not existing_user:
    # Insert the new user only if the user ID doesn't exist
        conn.execute(
            'INSERT INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)',
            (user.id, user.username, user.first_name, user.last_name)
        )
    conn.commit()
    conn.close()
    
    await update.message.reply_text(
        "Thank you! Your pet's profile has been created. You can update the details anytime."
    )
    
    logger.info("Activity reminder set for %s", user_data.get('pet_name'))
    await update.message.reply_text(
        "We're now setting daily reminders for your pet's morning and evening walks, post-walk feeding, and bedtime playtime to help keep your furry friend happy and healthy!"
    )
    await set_playtime_reminder(context, update.message.chat_id, user)
    
   
    
    # Check if any required fields are missing and set a reminder if necessary
    required_fields = ['breed', 'age', 'size']
    missing_fields = [field for field in required_fields if field not in context.user_data]
    if missing_fields:
        await update.message.reply_text(
            f"Some details are missing: {', '.join(missing_fields)}. You will be reminded to update your pet's details daily."
        )
        await set_reminder(context, update.message.chat_id)
        
    return ConversationHandler.END

async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s skipped a step.", user.first_name)
    current_state = context.user_data.get('current_state', BREED)
    if current_state == BREED:
        await update.message.reply_text(
            "Great! How old is your pet?",
            reply_markup=markup_age,
        )
        context.user_data['current_state'] = AGE
        return AGE
    elif current_state == AGE:
        await update.message.reply_text(
            "What is the size of your pet?",
            reply_markup=markup_size,
        )
        context.user_data['current_state'] = SIZE
        return SIZE
    elif current_state == SIZE:
        await update.message.reply_text(
            "Does your pet have any health issues?",
            reply_markup=markup_yes_no,
        )
        context.user_data['current_state'] = HEALTH_ISSUES
        return HEALTH_ISSUES
    elif current_state == HEALTH_ISSUES:
        await update.message.reply_text(
            "Does your pet have any allergies?",
            reply_markup=markup_yes_no,
        )
        context.user_data['current_state'] = ALLERGIES
        return ALLERGIES
    elif current_state == ALLERGIES:
        await update.message.reply_text(
            "Would you like to add any notes about your pet?",
            reply_markup=ReplyKeyboardRemove(),
        )
        context.user_data['current_state'] = NOTES
        return NOTES
    elif current_state == NOTES:
        await update.message.reply_text(
            "Thank you! Your pet's profile has been created. You can update the details anytime."
        )
        return ConversationHandler.END
    elif current_state == WEIGHT:
        await update.message.reply_text(
            "Please provide any other measurements for your pet (e.g. height, length).",
            reply_markup=ReplyKeyboardRemove(),
        )
        context.user_data['current_state'] = MEASUREMENTS
        return MEASUREMENTS
    elif current_state == MEASUREMENTS:
        await update.message.reply_text(
            "Now, let's set a playtime reminder for your pet. Please provide the frequency (e.g. 'daily', 'weekly', 'monthly') and the preferred time (e.g. 'morning', 'afternoon', 'evening')."
        )
        context.user_data['current_state'] = PLAYTIME
        return PLAYTIME
    else:
        await update.message.reply_text(
            "Thank you! Your pet's profile is now complete."
        )
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def get_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, pet_name)],
            BREED: [MessageHandler(filters.TEXT & ~filters.COMMAND, breed), CommandHandler("skip", skip)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age), CommandHandler("skip", skip)],
            SIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, size), CommandHandler("skip", skip)],
            # HEALTH_ISSUES: [MessageHandler(filters.TEXT & ~filters.COMMAND, health_issues), CommandHandler("skip", skip)],
            # ALLERGIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, allergies), CommandHandler("skip", skip)],
            # NOTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, notes), CommandHandler("skip", skip)],
            WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, weight), CommandHandler("skip", skip)],
            # MEASUREMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, measurements), CommandHandler("skip", skip)],
            # PLAYTIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, playtime), CommandHandler("skip", skip)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

def main() -> None:
    application = Application.builder().token("YOUR_TOKEN").build()

    conv_handler = get_conversation_handler()

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()