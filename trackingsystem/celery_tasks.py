from celery import Celery
from .tasks import send_reminder_email

# Create a Celery instance
app = Celery('trackingsystem')

# Schedule the task to run at the reminder_date
@app.task
def schedule_reminder_email(task_id, reminder_date):
    # Calculate the delay until the reminder_date
    delay = (reminder_date - datetime.now().date()).days
    if delay > 0:
        send_reminder_email.apply_async(args=[task_id], countdown=delay * 24 * 3600)  # Delay in seconds
