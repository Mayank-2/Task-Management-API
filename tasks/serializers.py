from .models import Task
from rest_framework import serializers
from account.models import User
from django.core.exceptions import ValidationError


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SerializerMethodField(required=False)
    def get_assigned_to(self, obj):
        return obj.assigned_to.email
    class Meta:
        model = Task
        fields = "__all__"



class UpdateTaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())

    class Meta:
        model = Task
        fields = "__all__"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def validate_status(self, value):

        task = self.instance
        if task:
            if task.status == 'pending' and value == "in-progress":
                return value
            elif task.status == 'in-progress' and value == "completed":
                return value
            elif task.status == 'completed' and value == "completed":
                return value
            elif value == "pending" and task.status in ["in-progress", "completed"]:
                raise ValidationError(
                    "Transition of status should be in logical flow")
            else:
                raise ValidationError("Invalid status transition.")
        return value
