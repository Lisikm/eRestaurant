from datetime import datetime, date, timedelta

import pytest
from django.contrib.auth.models import User, Group
from django.test import Client

from eMenu.models import Restaurant, OpeningHours, Menu, Dish, Note
from eReservation.models import Table, Reservation


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def owner_group():
    g = Group.objects.create(name='Owners')
    return g


@pytest.fixture
def owner_user(owner_group):
    u = User.objects.create(username='owner')
    u.set_password("qwe")
    u.save()
    u.groups.add(owner_group)
    return u


@pytest.fixture
def normal_user():
    u = User.objects.create(username='normal')
    u.set_password("qwe")
    u.save()
    return u


@pytest.fixture
def fake_restaurant_db(owner_user):
    owner = owner_user
    for x in range(1, 4):
        restaurant = Restaurant.objects.create(
            name=f"restaurant{x}",
            description=f"description{x}",
            category="American",
            user=owner,
            authorized=True
        )
        OpeningHours.objects.create(
            day_of_the_week=3,
            from_hour=x + 10,
            to_hour=x + 18,
            restaurant=restaurant,
        )
    return Restaurant.objects.all()


@pytest.fixture
def fake_menu_db(owner_user, fake_restaurant_db):
    restaurants = fake_restaurant_db
    owner = owner_user
    for z in range(0, 3):
        restaurant = restaurants[z]
        for x in range(1, 3):
            Menu.objects.create(
                name=f"menu{z + 1}-{x}",
                description=f"description{x}",
                restaurant=restaurant,
                user=owner,
                authorized=True
            )
    return Menu.objects.all()


@pytest.fixture
def fake_dish_db(owner_user, fake_menu_db):
    menus = fake_menu_db
    owner = owner_user
    for menu in menus:
        for x in range(1, 4):
            dish = Dish.objects.create(
                name=f"dish{x}",
                description=f"description{x}",
                price=x * 10,
                preparation_time=x * 10,
                is_wegetarian=True if x % 2 else False,
                user=owner
            )
            menu.dish_set.add(dish)
    return Dish.objects.all()


@pytest.fixture
def fake_note_db(normal_user, fake_restaurant_db):
    restaurants = fake_restaurant_db
    user = normal_user
    for restaurant in restaurants:
        for x in range(1, 3):
            Note.objects.create(
                title=f"title{x}",
                content=f"content{x}",
                email=f"fake{x}@fa.ke",
                restaurant=restaurant,
                user=user
            )
    return Note.objects.all()


@pytest.fixture
def fake_table_db(fake_restaurant_db):
    restaurants = fake_restaurant_db
    for restaurant in restaurants:
        for x in range(1, 3):
            Table.objects.create(
                name=f"name{x}",
                description=f"description{x}",
                seats=x,
                restaurant=restaurant
            )
    return Table.objects.all()


def next_wednesday():
    d = date.today() + timedelta(days=1)
    while d.weekday() != 2:
        d += timedelta(days=1)
    return d


@pytest.fixture
def fake_reservation_db(normal_user, fake_table_db):
    tables = fake_table_db
    user = normal_user
    for table in tables:
        for x in range(1, 3):
            Reservation.objects.create(
                from_hour=x + 12,
                to_hour=x + 13,
                date=next_wednesday(),
                table=table,
                user=user,
                description=f"description{x}"
            )
    return Reservation.objects.all()
