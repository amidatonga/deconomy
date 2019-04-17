from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fullname = models.CharField(max_length=50, default='Default Name')
    img = models.ImageField(default='default.jpg', upload_to='user_images')
    age = models.PositiveIntegerField(default='0')
    moderator = models.BooleanField(default=False)
    bio = models.TextField()

    def __str__(self):
        return f'Profile of {self.user.username}'

    def save(self, **kwargs):
        super().save()

        image = Image.open(self.img.path)
        if image.height > 128 or image.width > 128:
            resize = (128, 128)
            image.thumbnail(resize)
            image.save(self.img.path)
