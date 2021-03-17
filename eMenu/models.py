from django.db import models
from django.contrib.auth.models import User

CATEGORY = (
    ("American", "American"),
    ("Italian", "Italian"),
    ("Vietnamese", "Vietnamese"),
    ("Indian", "Indian"),
    ("Polish", "Polish"),
    ("Chinese", "Chinese"),
    ("Japanese", "Japanese"),
    ("Mexican", "Mexican")
)

DOTW = (
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday")
)

HOURS = (
    (1, "01:00"),
    (2, "02:00"),
    (3, "03:00"),
    (4, "04:00"),
    (5, "05:00"),
    (6, "06:00"),
    (7, "07:00"),
    (8, "08:00"),
    (9, "09:00"),
    (10, "10:00"),
    (11, "11:00"),
    (12, "12:00"),
    (13, "13:00"),
    (14, "14:00"),
    (15, "15:00"),
    (16, "16:00"),
    (17, "17:00"),
    (18, "18:00"),
    (19, "19:00"),
    (20, "20:00"),
    (21, "21:00"),
    (22, "22:00"),
    (23, "23:00"),
    (24, "24:00")
)


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORY, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    authorized = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class OpeningHours(models.Model):
    day_of_the_week = models.IntegerField(choices=DOTW)
    from_hour = models.IntegerField(choices=HOURS)
    to_hour = models.IntegerField(choices=HOURS)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('day_of_the_week', 'restaurant')
        ordering = ['day_of_the_week']


class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    add_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    authorized = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    preparation_time = models.IntegerField()
    add_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)
    is_wegetarian = models.BooleanField()
    menu = models.ManyToManyField(Menu)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-price', 'name']


class Note(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    email = models.EmailField()
    add_date = models.DateField(auto_now_add=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['add_date']