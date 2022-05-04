from django.db import models


# Create your models here.
class LoginPage(models.Model):
    title = models.CharField(max_length=60)
    background_image = models.ImageField()
