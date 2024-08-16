from django.db import models

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nivel = models.SmallIntegerField(default=0)
    phone_number = models.CharField(max_length=20, blank=True)
    theme = models.CharField(max_length=15, default='default')
    picture = models.ImageField(upload_to='user/pictures',
                                blank=True,
                                null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username