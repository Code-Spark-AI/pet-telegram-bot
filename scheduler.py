from croniter import croniter
from datetime import datetime
from telegram.ext import JobQueue, ContextTypes

base_time = datetime.now()

async def send_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the reminder message."""
    job = context.job
    await context.bot.send_message(chat_id=job.data['chat_id'], text=f"Reminder: {job.data['activity']}")

async def schedule_cron_job(job_queue: JobQueue, chat_id: int, activity: str, cron_expression: str) -> None:
    """Schedule a cron job based on the cron expression."""
    cron = croniter(cron_expression, base_time)
    
    async def cron_job(context: ContextTypes.DEFAULT_TYPE) -> None:
        """Wrapper for the cron job to send reminders."""
        await send_reminder(context)
        next_time = cron.get_next(datetime)
        job_queue.run_once(cron_job, next_time - datetime.now(), data=context.job.data)
    
    next_time = cron.get_next(datetime)
    job_queue.run_once(cron_job, next_time - datetime.now(), data={'chat_id': chat_id, 'activity': activity})