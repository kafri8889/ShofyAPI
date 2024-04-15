from django.db import models


class User(models.Model):

    name = models.CharField(max_length=200)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

    def __str__(self):
        return f"User(name={self.name}, username={self.username}, email={self.email})"


