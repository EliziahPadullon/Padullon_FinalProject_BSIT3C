from django.db import models

class Users(models.Model):
    username = models.CharField()
    password = models.CharField() 
    email = models.EmailField()
    name = models.CharField()