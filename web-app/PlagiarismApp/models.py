from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=12)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.username
