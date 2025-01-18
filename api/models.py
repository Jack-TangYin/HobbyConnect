from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    friends = models.ManyToManyField(
        'self', through='Friendship', symmetrical=False, related_name='related_friends'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def as_dict(self):
        dob = self.date_of_birth.strftime('%d/%m/%Y') if self.date_of_birth else None
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dateOfBirth': dob,
            'hobbies': [h.as_dict() for h in self.hobbies.all()],
            'friends': [
                {'id': friend.id, 'username': friend.username, 'email': friend.email}
                for friend in self.get_friends()
            ],
        }


    def get_friends(self):
        """
        Returns a queryset of all the user's friends.
        """
        friendships = Friendship.objects.filter(user1=self) | Friendship.objects.filter(user2=self)
        friend_ids = set()
        for friendship in friendships:
            friend_ids.add(friendship.user1_id if friendship.user2_id == self.id else friendship.user2_id)
        return CustomUser.objects.filter(id__in=friend_ids)

class Friendship(models.Model):
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='friendship_initiator', on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='friendship_receiver', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} ↔ {self.user2}"

class FriendRequest(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending',
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"
