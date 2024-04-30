from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models

from books.models import Book

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=0, related_name="profile")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    favorite_books = models.ManyToManyField(Book, blank=True)
    followed_users = models.ManyToManyField("self", blank=True, related_name="following", symmetrical=False)
    follower_users = models.ManyToManyField("self", blank=True, related_name="followers", symmetrical=False)
    feedback_results = models.JSONField(blank=True, null = True)

    def __str__(self):
        return str(self.user.id)
    
    def save(self, *args, **kwargs):
        if not isinstance(self.feedback_results, list):
            self.feedback_results = []  # Ensure feedback_results is always a list
        super(UserProfile, self).save(*args, **kwargs)
    