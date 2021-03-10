from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm, AddUserForm
from .models import Restaurant, Menu, Dish


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class ContactView(View):
    def get(self, request):
        return render(request, "contact.html")


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            if User.objects.filter(username=username):
                user = authenticate(username=username, password=form.cleaned_data['password'])
                if user:
                    login(request, user)
                    return redirect("home")
                else:
                    return render(request, "login.html", {"form": form, "error": "Wrong password"})
            return render(request, "login.html", {"form": form, "error": "User not found"})
        else:
            return render(request, "login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(request.META['HTTP_REFERER'])


class AddUserView(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, "adduser.html", {"form": form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data["login"],
                first_name=form.cleaned_data['name'],
                last_name=form.cleaned_data['surname'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            return redirect('login')
        return render(request, "adduser.html", {"form": form})


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
