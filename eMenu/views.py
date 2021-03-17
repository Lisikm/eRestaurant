from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import Restaurant, Menu, Note, OpeningHours, Dish
from .forms import NoteForm, AddRestaurantForm, AddRestaurantMenuForm, AddNewDishForm, AddExistingDishForm, \
    ModifyRestaurantMenuForm
from braces.views import GroupRequiredMixin


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class ErrorView(View):
    def get(self, request):
        error = "Something went wrong."
        return render(request, "error.html", {"error":error})


class ContactView(LoginRequiredMixin, View):
    def get(self, request, pk):
        form = NoteForm()
        return render(request, "contact.html", {"form": form})

    def post(self, request, pk):
        form = NoteForm(request.POST)
        if form.is_valid():
            note = Note.objects.create(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                email=form.cleaned_data['email'],
                restaurant=Restaurant.objects.get(pk=pk),
                user=request.user
            )
            return render(request, "succesnote.html", {"note":note})
        else:
            return render(request, "contact.html", {"form": form})


class RestaurantListView(View):
    def get(self, request):
        restaurants = Restaurant.objects.filter(authorized=True)
        return render(request, "restaurantlist.html", {"restaurants": restaurants})


class RestaurantView(View):
    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        return render(request, "restaurant.html", {"restaurant": restaurant})


class MenuListView(View):
    def get(self, request):
        menus = Menu.objects.filter(authorized=True)
        return render(request, "menulist.html", {"menus": menus})


class MenuView(View):
    def get(self, request, pk):
        menu = Menu.objects.get(pk=pk)
        return render(request, "menu.html", {"menu": menu})


class AddRestaurantView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request):
        form = AddRestaurantForm()
        return render(request, "addrestaurant.html", {"form": form})

    def post(self, request):
        form = AddRestaurantForm(request.POST)
        if form.is_valid():
            restaurant = Restaurant.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                user=request.user,
            )
            opening_hours = (
                (1, form.cleaned_data["monday_from"], form.cleaned_data["monday_to"]),
                (2, form.cleaned_data["tuesday_from"], form.cleaned_data["tuesday_to"]),
                (3, form.cleaned_data["wednesday_from"], form.cleaned_data["wednesday_to"]),
                (4, form.cleaned_data["thursday_from"], form.cleaned_data["thursday_to"]),
                (5, form.cleaned_data["friday_from"], form.cleaned_data["friday_to"]),
                (6, form.cleaned_data["saturday_from"], form.cleaned_data["saturday_to"]),
                (7, form.cleaned_data["sunday_from"], form.cleaned_data["sunday_to"]),
            )
            for day in opening_hours:
                OpeningHours.objects.create(
                    day_of_the_week=day[0],
                    from_hour=int(day[1]),
                    to_hour=int(day[2]),
                    restaurant=restaurant
                )
            return redirect('user-restaurants')
        return render(request, "addrestaurant.html", {"form": form})


class RestaurantUnauthorisedView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        if restaurant.user == request.user:
            restaurant.authorized = False
            restaurant.save()
            for menu in restaurant.menu_set.all():
                menu.authorized = False
                menu.save()
            return redirect("user-restaurants")
        return redirect("user-restaurants")


class AddRestaurantMenuView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, pk):
        form = AddRestaurantMenuForm()
        return render(request, "addmenu.html", {"form": form})

    def post(self, request, pk):
        form = AddRestaurantMenuForm(request.POST)
        if form.is_valid():
            Menu.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                restaurant=Restaurant.objects.get(pk=pk),
                user=request.user,
                authorized=False
            )
            return redirect('user-restaurants')
        return render(request, "addmenu.html", {"form": form})


class ModifyRestaurantMenuView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, pk):
        menu = Menu.objects.get(pk=pk)
        form = ModifyRestaurantMenuForm(initial={
            'name': menu.name,
            'description': menu.description,
            'authorized': menu.authorized
        })
        return render(request, "modifymenu.html", {"form": form, "menu": menu})

    def post(self, request, pk):
        menu = Menu.objects.get(pk=pk)
        form = ModifyRestaurantMenuForm(request.POST, instance=menu)
        if form.is_valid():
            menu.name = form.cleaned_data['name']
            menu.description = form.cleaned_data['description']
            if not menu.restaurant.authorized:
                if form.cleaned_data['authorized']:
                    return render(request, "modifymenu.html", {"form": form, "menu": menu,
                                                               "error":"You can not set menu to authorized "
                                                                       "when restaurant is unauthorized."})
            else:
                menu.authorized = form.cleaned_data['authorized']
            menu.save()
            return redirect('user-restaurants')
        return render(request, "modifymenu.html", {"form": form, "menu": menu})


class DeleteRestaurantMenuView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, pk):
        menu = Menu.objects.get(pk=pk)
        if menu.user == request.user:
            menu.delete()
            return redirect("user-restaurants")
        return redirect("user-restaurants")


class DishView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, pk):
        dish = Dish.objects.get(pk=pk)
        return render(request, "dish.html", {"dish":dish})


class AddNewDishView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, pk):
        form = AddNewDishForm()
        return render(request, "addnewdish.html", {"form": form})

    def post(self, request, pk):
        form = AddNewDishForm(request.POST)
        if form.is_valid():
            dish = Dish.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                price=form.cleaned_data["price"],
                preparation_time=form.cleaned_data["preparation_time"],
                is_wegetarian=form.cleaned_data["is_wegetarian"],
                user=request.user,
            )
            menu = Menu.objects.get(pk=pk)
            menu.dish_set.add(dish)
            return redirect("menu-modify", pk)
        return render(request, "addnewdish.html", {"form": form})


class ModifyDishView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, pk):
        dish = Dish.objects.get(pk=pk)
        form = AddNewDishForm(initial={
            "name": dish.name,
            "description": dish.description,
            "price": dish.price,
            "preparation_time":dish.preparation_time,
            "is_wegetarian":dish.is_wegetarian
        })
        return render(request, "modifydish.html", {"form": form})

    def post(self, request, pk):
        dish = Dish.objects.get(pk=pk)
        form = AddNewDishForm(request.POST, instance=dish)
        if form.is_valid():
            dish.name = form.cleaned_data["name"]
            dish.description = form.cleaned_data["description"]
            dish.price = form.cleaned_data["price"]
            dish.preparation_time = form.cleaned_data["preparation_time"]
            dish.is_wegetarian = form.cleaned_data["is_wegetarian"]
            dish.save()
            return redirect("dish", dish.id)
        return render(request, "modifydish.html", {"form": form})


class RemoveFromMenuView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, m_pk, d_pk):
        try:
            dish = Dish.objects.get(pk=d_pk)
            menu = Menu.objects.get(pk=m_pk)
        except:
            return redirect("error")
        if dish in menu.dish_set.all():
            menu.dish_set.remove(dish)
            return redirect("menu-modify", m_pk)
        else:
            return redirect("error")


class AddExistingDishToMenuView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, pk):
        form = AddExistingDishForm(user=request.user)
        menu = Menu.objects.get(pk=pk)
        return render(request, "addexistingdish.html", {"form":form, "menu":menu})

    def post(self, request, pk):
        form = AddExistingDishForm(request.POST, user=request.user)
        menu = Menu.objects.get(pk=pk)
        if form.is_valid():
            dish = form.cleaned_data['dishes']
            menu.dish_set.add(dish)
            return redirect("menu-modify", pk)
        return render(request, "addexistingdish.html", {"form": form, "menu": menu})
