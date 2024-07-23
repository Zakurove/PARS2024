from accounts.models import CustomUser
from django.db import models
from datetime import datetime , timedelta
from django.utils import timezone




category_list = [
    ("s", "Safety stock"),
    ("p", "Pipeline Stock" ),
    ("a", "Anticipatory Stock"),
    ("d", "Decoupling Stock"),
]

# Changed it so we can filter it based on dept with ease.
department_list = [
    ("Vender department", "Vender department"),
    ("Tender department", "Tender department"),
    ("Financial department", "Financial department"),
]

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=[('customer', 'Customer'), ('employee', 'Employee')])

    # Add more fields as needed

    def __str__(self):
        return self.user.username


class Department(models.Model):
    name = models.CharField(max_length=100)

class Item(models.Model):
    name = models.CharField(max_length=100)

class ApprovalStage(models.Model):
    name = models.CharField(max_length=100)
    approvers = models.ManyToManyField(CustomUser)

class PARRequest(models.Model):
    Par_status = [
    ("pending", "pending"),
    ("approved", "approved"),
    ("expired", "expired"),
]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=50, choices=department_list)
    item = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    status = models.CharField(null=True, max_length=50, choices=Par_status, default="pending")
    attachment = models.FileField(upload_to='par_requests/', null=True, blank=True)
    signed_attachment = models.FileField(upload_to='signed_par_requests/', null=True, blank=True)
    category = models.CharField(max_length=50, null=True, choices=category_list)
    unite_price = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    chosen_date = models.DateField(null=True)
    was_approved = models.BooleanField(default=False)
    was_pending = models.BooleanField(default=True)
    was_expired = models.BooleanField(default=False)


    def calculate_duration(self):
        if self.created_at and self.chosen_date:
            duration = self.chosen_date - self.created_at.date()
            return duration
        return None

    reminder_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate the reminder date 10 days before the chosen date
        if not self.reminder_date:
            self.reminder_date = self.chosen_date - timedelta(days=10)
        super(PARRequest, self).save(*args, **kwargs)






class EmailTask(models.Model):
    recipient = models.EmailField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)
    send_at = models.DateTimeField()

