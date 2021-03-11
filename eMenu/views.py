from django.shortcuts import render
from django.views import View
from .models import Restaurant, Menu


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class ContactView(View):
    def get(self, request):
        return render(request, "contact.html")


class RestaurantListView(View):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        return render(request, "restaurantlist.html", {"restaurants":restaurants})


class RestaurantView(View):
    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        return render(request, "restaurant.html", {"restaurant":restaurant})


class MenuListView(View):
    def get(self, request):
        menus = Menu.objects.all()
        return render(request, "menulist.html", {"menus":menus})


class MenuView(View):
    def get(self, request, pk):
        menu = Menu.objects.get(pk=pk)
        return render(request, "menu.html", {"menu":menu})
