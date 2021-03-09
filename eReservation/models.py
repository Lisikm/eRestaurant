from django.db import models
from eMenu.models import Restaurant, HOURS
from django.contrib.auth.models import User


class Table(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=255)
    seats = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'restaurant')


class Reservation(models.Model):
    from_hour = models.IntegerField(choices=HOURS)
    to_hour = models.IntegerField(choices=HOURS)
    date = models.DateField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ['date', 'from_hour']