from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get-stations-json", views.get_all_stations_json, name="get stations json"),
]