from django.db.models import Model
from django.db import models


# Create your models here.
class List(Model):
    pass


class Item(Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
