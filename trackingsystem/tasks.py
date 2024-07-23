from celery import shared_task
from datetime import datetime
from django.core.mail import send_mail
from .models import PARRequest

@shared_task
def send_reminder_email(task_id):

    par_request = PARRequest.objects.create(chosen_date=chosen_date, reminder_date=reminder_date)
    schedule_reminder_email.delay(par_request.id, par_request.reminder_date)

    # Check if the reminder_date has passed
    if datetime.now().date() >= par_request.reminder_date:
        subject = 'Reminder for PAR Request'
        message = 'This is a reminder for your PAR Request.'
        recipient_list = [par_request.email]  # Replace with the recipient's email address
        send_mail(subject, message, 'your-email@example.com', recipient_list)
