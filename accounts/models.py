"""
File: models.py
Author: Reagan Zierke <reaganzierke@gmail.com>
Date: 2025-10-25
Description: Models for the accounts app.
"""


from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Custom user manager where email is the unique identifier."""
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with email as the unique identifier."""
    username = None  
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return (self.first_name + " " + self.last_name).strip()

class Profile(models.Model):
    """User profile model to store additional information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    height = models.FloatField(blank=True, null=True)  
    weight = models.FloatField(blank=True, null=True)  
    location = models.CharField(max_length=255, blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    competition_date = models.DateField(blank=True, null=True, help_text="Date of next competition")
    desired_weight_class = models.CharField(max_length=50, blank=True, null=True, )
    training_environment = models.CharField(max_length=255, blank=True, null=True)
    lifting_gear = models.BooleanField(default=False)
    recent_training_log = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}'s Profile"

    def save(self, *args, **kwargs):
        if self.dob:
            from datetime import date
            today = date.today()
            self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        super().save(*args, **kwargs)

class Experience(models.Model):
    """User experience model to store training background."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    level = models.CharField(max_length=100)
    time_lifted = models.CharField(max_length=100)
    current_program = models.CharField(max_length=255)
    days_per_week = models.PositiveIntegerField()
    preffered_days = models.CharField(max_length=255)
    squat_est = models.FloatField()  # estimated 1RM
    bench_est = models.FloatField()  # estimated 1RM
    deadlift_est = models.FloatField()  # estimated 1RM

    def __str__(self):
        return f"{self.user}'s Experience"
    
class PreviousCoach(models.Model):
    """Model to store previous coaches."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='previous_coaches')
    coach_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user}'s Previous Coach: {self.coach_name}"
    
class Nutrition(models.Model):
    """Nutrition model to store user's nutrition information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nutrition')
    plan = models.BooleanField(default=False)
    calories_per_day = models.PositiveIntegerField(blank=True, null=True)
    protein_per_day = models.FloatField(blank=True, null=True)  # in grams
    weight_management = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., cutting, bulking, maintenance")
    sleep_habits = models.PositiveIntegerField(blank=True, null=True)  # hours per night    
    stress = models.CharField(max_length=50, blank=True, null=True)
    supplements = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}'s Nutrition Info"

class Goal(models.Model):
    """Goal model to store user's goals."""
    GOAL_TYPE_CHOICES = [
        ('short_term', 'Short Term'),
        ('long_term', 'Long Term'),
        ('primary', 'Primary'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    type = models.CharField(max_length=100, choices=GOAL_TYPE_CHOICES)
    description = models.TextField()   

    def __str__(self):
        return f"{self.user}'s Goal: {self.type}"

class Injury(models.Model):
    """Injury model to store user's injury information."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='injuries')
    started = models.DateField()
    ended = models.DateField(blank=True, null=True)
    info = models.TextField()
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}'s Injury starting {self.started}"

    def save(self, *args, **kwargs):
        if self.ended:
            self.resolved = True
        super().save(*args, **kwargs)

class CoachingPreference(models.Model):
    """Coaching preference model to store user's coaching preferences."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coaching_preference')
    style = models.CharField(max_length=100, blank=True, null=True)
    check_in_frequency = models.CharField(max_length=100, blank=True, null=True)
    video_analysis = models.BooleanField(default=False)
    communication_method = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user}'s Coaching Preference"

class Equipment(models.Model):
    """Equipment model to store user's equipment."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='equipment')
    piece_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user}'s Equipment: {self.piece_name}"

class VideoLink(models.Model):
    """Video link model to store user's video links."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_links')
    link = models.URLField()

    def __str__(self):
        return f"{self.user}'s Video Link"

class SocialMedia(models.Model):
    """Social media model to store user's social media links."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='social_media')
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}'s Social Media Links"
    

class Health(models.Model):
    """Health model to store user's health information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health')
    conditions = models.TextField(blank=True, null=True, help_text="List any health conditions")
    mobility_issues = models.TextField(blank=True, null=True, help_text="List any mobility issues")
    cleared_for_training = models.BooleanField(default=True)