from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from account.models import User
import uuid
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
STATUS_CHOICES = [
    ('pending', 'pending'),
    ('in-progress', 'in-progress'),
    ('completed', 'completed'),
]
PRIORITY_CHOICES = [
    ('low', 'low'),
    ('medium', 'medium'),
    ('high', 'high')
]


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, blank=True, null=True, default="")
    description = models.TextField(blank=True, null=True, default="")
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(
        max_length=30, choices=PRIORITY_CHOICES, default="low")
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    
    def date_validate(self):
        if self.due_date < now().date():
            raise ValidationError("Due date cannot be in the past.")
        return True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.date_validate()
        super().save(*args, **kwargs)
