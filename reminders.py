from telegram import Update
from telegram.ext import ContextTypes
import pytz
from datetime import time
from db import get_db_connection

# List of time configurations (hour, minute) for reminders
feed_time = [
    (8, 0),   # 8:00 AM
    (19, 0)   # 7:00 PM
]

walk_time = [
    (7, 0),   # 7:00 AM
    (18, 0)   # 6:00 PM
]

play_time = [
    (21, 0)   # 9:00 PM
]

# Days for which the reminders should run (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
days = (0, 1, 2, 3, 4, 5, 6)

def insert_reminder_details(conn, user_id, pet_id, activity, time, cron_expression):
    conn.execute(
        'INSERT INTO reminders (user_id, pet_id, activity, time, cron_expression) VALUES (?, ?, ?, ?, ?)',
        (user_id, pet_id, activity, time, cron_expression)
    )
    conn.commit()

async def remind_update_details(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    user_data = context.bot_data.get(job.chat_id, {})
    
    required_fields = ['breed', 'age']
    missing_fields = [field for field in required_fields if field not in user_data]

    if missing_fields:
        await context.bot.send_message(
            job.chat_id, 
            text=f"Don't forget to update your pet's details! Missing: {', '.join(missing_fields)}"
        )
    else:
        await context.bot.send_message(
            job.chat_id, 
            text="Your pet's profile is complete. No further updates needed."
        )
        job.schedule_removal()

async def set_reminder(context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> None:
    context.job_queue.run_repeating(remind_update_details, interval=100, first=0, chat_id=chat_id)

async def set_playtime_reminder(context: ContextTypes.DEFAULT_TYPE, chat_id: int, user: any) -> None:
    pet_name = context.bot_data[user.id].get('pet_name')
    context.bot_data['user_id'] = user.id
    # Iterate through time configurations and schedule the jobs
    for hour, minute in walk_time:
        name=f"walk_{hour}_{minute}"
        reminder_time = time(hour=hour, minute=minute, tzinfo=pytz.timezone('Asia/Kolkata'))
        context.job_queue.run_daily(remind_walk, reminder_time, days=days, chat_id=chat_id, name=name)
        # insert_reminder_details(conn, context.user_data['user_id'], context.user_data['pet_id'], name, reminder_time)
        
    for hour, minute in feed_time:
        name=f"feed_{hour}_{minute}"
        reminder_time = time(hour=hour, minute=minute, tzinfo=pytz.timezone('Asia/Kolkata'))
        context.job_queue.run_daily(remind_feed, reminder_time, days=days, chat_id=chat_id, name=name)
        # insert_reminder_details(conn, context.user_data['user_id'], context.user_data['pet_id'], name, reminder_time)
        
    for hour, minute in play_time:
        name=f"play_{hour}_{minute}"
        reminder_time = time(hour=hour, minute=minute, tzinfo=pytz.timezone('Asia/Kolkata'))
        context.job_queue.run_daily(remind_playtime, reminder_time, days=days, chat_id=chat_id, name=name)
        # insert_reminder_details(conn, context.user_data['user_id'], context.user_data['pet_id'], name, reminder_time)
    # conn = get_db_connection()
    # conn.close()
    await context.bot.send_message(chat_id, text=f"Reminder set for your {pet_name}'s Health and Well-being activities.")

async def remind_feed(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    user_id = context.bot_data.get('user_id')
    pet_name = context.bot_data[user_id].get('pet_name')
    await context.bot.send_message(job.chat_id, text=f"It's time for your {pet_name}'s to cool down and ready for a nutritious meal!")
    
async def remind_walk(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    user_id = context.bot_data.get('user_id')
    pet_name = context.bot_data[user_id].get('pet_name')
    await context.bot.send_message(job.chat_id, text=f"It's time for your {pet_name}'s walk! Perfect way for your pet to unwind and get some exercise.")
    
async def remind_playtime(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    user_id = context.bot_data.get('user_id')
    pet_name = context.bot_data[user_id].get('pet_name')
    await context.bot.send_message(job.chat_id, text=f"It's time for your {pet_name}'s playtime activity! This helps them relax and have a good night's sleep.")


