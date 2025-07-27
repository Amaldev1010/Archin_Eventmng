
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Custom user model with role-based access
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('coordinator', 'Coordinator'),
        ('participant', 'Participant'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional field
    department = models.CharField(max_length=100, blank=True, null=True)  # Optional field
    year_of_study = models.CharField(max_length=4, blank=True, null=True)  # Optional field, e.g., "2023"
    college_name = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return f"{self.username} ({self.role})"

# Event model created by a Coordinator
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    coordinator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_events')

    registered_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='registered_events', blank=True)

    def __str__(self):
        return self.title

# Registration model linking Participant with an Event
class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # Prevent duplicate registrations

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"
