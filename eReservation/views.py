from django.shortcuts import render
from django.views import View
from datetime import date, timedelta
from .models import Table, Reservation
from eMenu.models import Restaurant


class TableListView(View):
    def get(self, request, pk):
        tables = Table.objects.filter(restaurant_id=pk)
        return render(request, "tablelist.html", {"tables": tables})


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


def next_seven_days():
    n7d = []
    for el in range(1, 8):
        next_day = date.today() + timedelta(days=el)
        next_day_weekday = next_day.weekday()
        next_day_weekday_string = DOTWDICT[next_day_weekday]
        n7d.append([next_day, next_day_weekday_string, next_day_weekday + 1])
    return n7d


class TableReservationView(View):
    def get(self, request, pk):
        table = Table.objects.get(pk=pk)
        next7d = next_seven_days()
        next_days = []
        for elem in next7d:
            valid = False
            for ele in table.restaurant.openinghours_set.all():
                if (elem[2]) == ele.day_of_the_week:
                    valid = True
                    break
            if valid:
                from_hour = table.restaurant.openinghours_set.filter(day_of_the_week=elem[2])[0].from_hour
                to_hour = table.restaurant.openinghours_set.filter(day_of_the_week=elem[2])[0].to_hour
                elem.append([HOURSDICT[x] for x in range(from_hour, to_hour)])
                elem.append([])
                next_days.append(elem)
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


class MakeReservationView(View):
    def get(self, request, pk):
        restaurant = Restaurant.objects.get(pk=pk)
        next7d = next_seven_days()
        next_days = []
        for elem in next7d:
            valid = False
            for ele in restaurant.openinghours_set.all():
                if (elem[2]) == ele.day_of_the_week:
                    valid = True
                    break
            if valid:
                next_days.append(elem)

        return render(request, "makereservation.html", {"restaurant":restaurant, "next_days":next_days})