from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from eMenu.models import Restaurant, Note
from eReservation.models import Reservation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, AddUserForm


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
                    next_url = request.GET.get("next", None)
                    if next_url is None:
                        return redirect("user-panel")
                    else:
                        return redirect(next_url)
                else:
                    return render(request, "login.html", {"form": form, "error": "Wrong password"})
            return render(request, "login.html", {"form": form, "error": "User not found"})
        else:
            return render(request, "login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("home")


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


class UserPanelView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "userpanel.html")


class UserRestaurantsView(GroupRequiredMixin, View):
    group_required = (u"Owners",)

    def get(self, request):
        restaurants = Restaurant.objects.filter(user=request.user)
        return render(request, "userrestaurants.html", {"restaurants":restaurants})


class UserReservationsView(LoginRequiredMixin, View):
    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user)
        return render(request, "userreservations.html", {"reservations":reservations})


class UserRestaurantNotesView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, pk):
        notes = Note.objects.filter(restaurant_id=pk)
        return render(request, "restaurantnotes.html", {"notes":notes})


class UserRestaurantNoteDeleteView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)
        except:
            return redirect("error")
        if note.restaurant.user == request.user:
            note_restaurant = note.restaurant
            note.delete()
            return redirect("restaurant-notes", note_restaurant.id)
        else:
            return redirect("error")

