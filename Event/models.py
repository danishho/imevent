from django.db import models
from datetime import date
# Create your models here.
from django.contrib.auth.models import AbstractUser

USER_TYPE_CHOICES = (
    ('student', 'Student'),
    ('Mpp', 'MPP'),
    ('Admin', 'Admin')
)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def save(self, *args, **kwargs):
        # If the user is a superuser set the user_type to admin
        if self.is_superuser:
            self.user_type = 'Admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images/')
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    max_tickets = models.PositiveIntegerField()
    tags = models.ManyToManyField(Tag, related_name='events', blank=True)
    created_by = models.ForeignKey(CustomUser, related_name='created_events', on_delete=models.CASCADE, limit_choices_to={'user_type': 'mpp'})

    def __str__(self):
        return self.title


class Booking(models.Model):
    book_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    booking_date = models.DateField(auto_now_add=True)
    event = models.ForeignKey(Event, related_name='bookings', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='bookings', on_delete=models.CASCADE)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.event.title}"