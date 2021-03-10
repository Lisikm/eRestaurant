"""eRestaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from eMenu.views import HomeView, LoginView, LogoutView, AddUserView, RestaurantListView, RestaurantView, MenuListView,\
    MenuView, ContactView
from eReservation.views import TableListView, TableReservationsView, ReservationDateView, ReserveTableView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add_user/', AddUserView.as_view(), name='add-user'),
    path('restaurant/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurant/<int:pk>/', RestaurantView.as_view(), name='restaurant'),
    path('menu/', MenuListView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', MenuView.as_view(), name='menu'),
    path('tables/<int:pk>/', TableListView.as_view(), name='table-list'),
    path('table/<int:pk>/reservations/', TableReservationsView.as_view(), name='table-reservations'),
    path('restaurant/<int:pk>/reservation_date/', ReservationDateView.as_view(), name='reservation-date'),
    path('restaurant/<int:pk>/<str:day>/<int:hour>/', ReserveTableView.as_view(), name='reserve-table'),

]
