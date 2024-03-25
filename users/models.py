from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 100, null=True)
    phone_number = models.IntegerField(default = 0)
    birthday = models.DateField()
    date_of_creation = models.DateField(auto_now_add = True, editable = False)
    objects = models.Manager()

    user = models.OneToOneField(User, on_delete= models.CASCADE, null = True)

    def __str__(self):
        return self.name
    