from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from datetime import date, timedelta

from .forms import AddTableForm
from .models import Table, Reservation
from eMenu.models import Restaurant, OpeningHours
import re

DOTWDICT = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

HOURSDICT = {
    1: "01:00",
    2: "02:00",
    3: "03:00",
    4: "04:00",
    5: "05:00",
    6: "06:00",
    7: "07:00",
    8: "08:00",
    9: "09:00",
    10: "10:00",
    11: "11:00",
    12: "12:00",
    13: "13:00",
    14: "14:00",
    15: "15:00",
    16: "16:00",
    17: "17:00",
    18: "18:00",
    19: "19:00",
    20: "20:00",
    21: "21:00",
    22: "22:00",
    23: "23:00",
    24: "00:00"
}

MONTHDICT = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}


def month_by_dict_value(month):
    for key, value in MONTHDICT.items():
        if month == value:
            return key
    return None


def next_seven_days():
    n7d = []
    for el in range(1, 8):
        next_day = date.today() + timedelta(days=el)
        next_day_weekday = next_day.weekday()
        next_day_weekday_string = DOTWDICT[next_day_weekday]
        n7d.append([next_day, next_day_weekday_string, next_day_weekday + 1])
    return n7d


def next_opening_days(restaurant):
    next7d = next_seven_days()
    next_days = []
    for elem in next7d:
        valid = False
        for ele in restaurant.openinghours_set.all():
            if (elem[2]) == ele.day_of_the_week:
                valid = True
                break
        if valid:
            from_hour = restaurant.openinghours_set.filter(day_of_the_week=elem[2])[0].from_hour
            to_hour = restaurant.openinghours_set.filter(day_of_the_week=elem[2])[0].to_hour
            elem.append([(HOURSDICT[x]) for x in range(from_hour, to_hour)])
            next_days.append(elem)
    return next_days


def day_in_next_days(day, next_days):
    valid = False
    for elem in next_days:
        date = str(elem[0])
        if day == date:
            valid = True
    return valid


def hour_in_day(next_days, day, hour):
    valid = False
    for elem in next_days:
        date = str(elem[0])
        if day == date:
            if HOURSDICT[hour] in elem[3]:
                valid = True
    return valid


def tables_possible_to_reserve(restaurant, day, hour):
    """Returning array with tables and possible duration of reservation"""
    opening_hours = OpeningHours.objects.get(
        restaurant=restaurant,
        day_of_the_week=(date(int(day[:4]), int(day[5:7]), int(day[8:10])).weekday() + 1))
    all_tables = restaurant.table_set.filter(seats__lte=4)
    tables_reservations = []
    tables = []
    for elem in all_tables:
        table = elem
        reservations = elem.reservation_set.filter(date=day)
        tables_reservations.append([table, reservations])
    for elem in tables_reservations:
        hours_reserved = []
        for el in elem[1]:
            for x in range(el.from_hour, el.to_hour):
                hours_reserved.append(HOURSDICT[x])
        if HOURSDICT[hour] not in hours_reserved:
            biggest_hour = hour  # first biggest hour greater than reservation hour
            for el in hours_reserved:
                if int(el[:2]) > biggest_hour:
                    biggest_hour = int(el[:2])
                    break
            if biggest_hour == hour:
                if biggest_hour == opening_hours.to_hour - 1:
                    res_duration = [1]
                else:
                    res_duration = [1, 2]
            elif biggest_hour - hour >= 2:
                res_duration = [1, 2]
            else:
                res_duration = [1]
            tables.append([elem[0], res_duration])
    return tables


class TableListView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        tables = Table.objects.filter(restaurant=restaurant)
        return render(request, "tablelist.html", {"tables": tables, "restaurant":restaurant})


class TableReservationsView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, pk):
        table = Table.objects.get(pk=pk)
        restaurant = table.restaurant
        next_days = next_opening_days(restaurant)
        for elem in next_days:
            elem.append([])
        reservations = table.reservation_set.all()
        for elem in reservations:
            for ele in next_days:
                if ele[0] == elem.date:
                    for x in range(elem.from_hour, elem.to_hour):
                        ele[4].append(HOURSDICT[x])
        return render(request, "tablereservation.html", {
            "table": table,
            "next_days": next_days,
        })


class ReservationDateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        next_days = (next_opening_days(restaurant))
        for next_day in next_days:
            possible_hours = next_day.pop(3)
            new_possible_hours = []
            for possible_hour in possible_hours:
                day = str(next_day[0])
                possible_hour = int(possible_hour[:2])
                tables = tables_possible_to_reserve(restaurant, day=day, hour=possible_hour)
                if len(tables) != 0:
                    new_possible_hours.append(HOURSDICT[possible_hour])
            if len(new_possible_hours) != 0:
                next_day.append(new_possible_hours)
        return render(request, "makereservation.html", {"restaurant": restaurant, "next_days": next_days})

    def post(self, request, pk):
        day = request.POST.get("day")
        hour = request.POST.get("hour")
        restaurant = Restaurant.objects.get(pk=pk)
        next_days = (next_opening_days(restaurant))
        error = "Something went wrong. Please select date and hour again."
        if day and hour:
            try:
                day = day.split()
                day = f"{day[2]}-{month_by_dict_value(day[0])}-{day[1][:-1]}"
                hour = int(hour[:2])
            except:
                return render(request, "makereservation.html", {"restaurant": restaurant, "next_days": next_days,
                                                                "error": error})
            if re.fullmatch("^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$", day) and hour in HOURSDICT:
                day_valid = day_in_next_days(day, next_days)
                hour_valid = hour_in_day(next_days, day, hour)
                if not day_valid or not hour_valid:
                    return render(request, "makereservation.html", {"restaurant": restaurant, "next_days": next_days,
                                                                    "error": error})
                return redirect("reserve-table", pk, day, hour)
        return render(request, "makereservation.html", {"restaurant": restaurant, "next_days": next_days,
                                                        "error": error})


class ReserveTableView(LoginRequiredMixin, View):
    def get(self, request, pk, day, hour):
        restaurant = Restaurant.objects.get(pk=pk)
        next_days = (next_opening_days(restaurant))
        error = "Something went wrong."
        if re.fullmatch("^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$", day) and hour in HOURSDICT:
            day = day
            hour = hour
            day_valid = day_in_next_days(day, next_days)
            hour_valid = hour_in_day(next_days, day, hour)
            if not day_valid or not hour_valid:
                return render(request, "error.html", {"error": error})
            tables = tables_possible_to_reserve(restaurant,day,hour)
            return render(request, "reservetable.html", {"restaurant": restaurant, "day": day,
                                                         "hour": HOURSDICT[hour], "tables": tables})
        return render(request, "error.html", {"error": error})

    def post(self, request, pk, day, hour):
        error = "Something went wrong."
        restaurant = Restaurant.objects.get(pk=pk)
        duration = request.POST.get("duration")
        table_id = request.POST.get("table")
        description = request.POST.get("description")
        if description:
            if len(description) > 255:
                description = description[:255]
        else:
            description = ""
        if duration and table_id:
            try:
                duration = int(duration)
                table = Table.objects.get(pk=table_id)
            except:
                return render(request, "error.html", {"error": error})
            tables = tables_possible_to_reserve(restaurant, day, hour)
            table_valid = False
            duration_valid = False
            for elem in tables:
                if table == elem[0]:
                    table_valid = True
                    if duration in elem[1]:
                        duration_valid = True
                        break
            if not table_valid or not duration_valid:
                return render(request, "error.html", {"error": error})
            reservation = Reservation.objects.create(
                from_hour=hour,
                to_hour=hour+duration,
                date=day,
                description=description,
                table=table,
                user=request.user
            )
            return render(request, "successreservation.html", {"reservation": reservation})
        return render(request, "error.html", {"error": error})


class AddRestaurantTableView(GroupRequiredMixin, View):
    group_required = u"Owners"

    def get(self, request, pk):
        form = AddTableForm()
        return render(request, "addtable.html", {"form":form})

    def post(self, request, pk):
        form = AddTableForm(request.POST)
        restaurant = Restaurant.objects.get(pk=pk)
        if form.is_valid():
            Table.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                seats=form.cleaned_data["seats"],
                restaurant=restaurant
            )
            return redirect("table-list", restaurant.id)
        return render(request, "addtable.html", {"form": form})