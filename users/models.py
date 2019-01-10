from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(default='default.jpg', upload_to='user_images')
    age = models.PositiveIntegerField(default='0')
    copywriter = models.BooleanField(default=False)
    bio = models.TextField()

    def __str__(self):
        return f'Profile of {self.user.username}'
