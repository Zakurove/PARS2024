from django_cron import CronJobBase, Schedule

from .models import EmailTask
from django.core.mail import send_mail

class SendScheduledEmails(CronJobBase):
    RUN_EVERY_MINS = 1  # Adjust this to your desired frequency

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'your_app.send_scheduled_emails'  # Change 'your_app' to your app's name

    def do(self):
        current_time = timezone.now()
        pending_emails = EmailTask.objects.filter(send_at__lte=current_time, sent=False)

        for email_task in pending_emails:
            send_mail(
                email_task.subject,
                email_task.message,
                'your-email@example.com',  # From email
                [email_task.recipient],  # To email
                fail_silently=False,
            )
            email_task.sent = True
            email_task.save()
