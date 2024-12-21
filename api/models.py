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

class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
    
    
class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class CustomUser(AbstractUser):
    # The AbstractUser model already includes username, password, email, first_name, last_name
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    
    # Optionally, __str__ method can be customized
    def __str__(self):
        return self.username
    
    
    
    
    
    
    
    
    
    
    