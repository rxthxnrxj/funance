from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    age = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_interaction = models.DateTimeField(null=True, blank=True)
    last_intriguer_shown = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=50, default='NA')

class Intriguer(models.Model):
    text = models.TextField()
    theme = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)
    chunk = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    times_shown = models.IntegerField(default=0)
    last_shown = models.DateTimeField(null=True, blank=True)
    thumbnail = models.ImageField(
        null=True, blank=True, default='/brandPlaceholder.jpg')

    def __str__(self):
        return str(self.text)[:20]

class UserIntriguerInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    intriguer = models.ForeignKey(Intriguer, on_delete=models.CASCADE)
    shown_at = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)
    liked = models.BooleanField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'intriguer')

