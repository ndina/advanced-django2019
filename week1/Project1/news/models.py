from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Stuff(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)


class StuffStockDetails(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    due_on = models.DateTimeField()
    status = models.CharField(max_length=50)
    stuff_detail = models.ForeignKey(Stuff, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.due_on, self.name)
