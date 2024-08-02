from django.db import models
from django.utils import timezone
# from oauth2_provider.models import Application
import uuid

# class CustomApplication(Application):
#     clientid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     clientsecret = models.CharField(max_length=255, blank=True, null=True)

#     def save(self, *args, **kwargs):
#         if not self.clientsecret:
#             self.clientsecret = uuid.uuid4().hex
#         super().save(*args, **kwargs)


class APIKey(models.Model):
    key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.key

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    grade = models.CharField(max_length=10)
    major = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

