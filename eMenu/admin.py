from django.contrib import admin

from .models import Restaurant, Menu, Dish, OpeningHours

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Dish)
admin.site.register(OpeningHours)