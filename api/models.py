# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class PageView(models.Model):
#     count = models.IntegerField(default=0)

#     def __str__(self):
#         return f"Page view count: {self.count}"

# class CustomUser(AbstractUser):
#     # The AbstractUser model already includes username, password, email, first_name, last_name
#     # We can add additional fields:
#     date_of_birth = models.DateField(null=True, blank=True)
#     hobbies = models.TextField(blank=True, help_text="Enter your hobbies separated by commas")
    
#     # Optionally, you can customize __str__ method
#     def __str__(self):
#         return self.username





from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.dateformat import format as format_date

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
            'hobbies': [hobby.as_dict() for hobby in self.hobbies.all()]
        }