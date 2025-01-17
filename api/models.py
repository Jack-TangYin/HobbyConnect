from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.dateformat import format as format_date
from django.conf import settings

class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
    
    
class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        """Return the name of the hobby"""
        return self.name
    
    def as_dict(self):
        """Return the hobby as a dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    

class CustomUser(AbstractUser):
    # The AbstractUser model already includes username, password, email, first_name, last_name
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    friends = models.ManyToManyField('self', blank=True)
    
    # Optionally, __str__ method can be customized
    def __str__(self):
        """Return the first and last name of the user"""
        return f"{self.first_name} {self.last_name}"
    
    def as_dict(self):
        """Return the user as a dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dateOfBirth': format_date(self.date_of_birth, "d F, Y") if self.date_of_birth else None,
            'hobbies': [hobby.as_dict() for hobby in self.hobbies.all()],
            'friends': [CustomUser.as_dict() for friend in self.friends.all()]
        }
    

class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"