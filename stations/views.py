from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import EnciclaStation


def index(request):
    stations = list()
    for station in EnciclaStation.objects.values():
        stations.append({
            'name': station['name'],
            'address': station['address'],
            'capacity': station['capacity'],
            'status': station['status'],
            'latitude': station['geom'].y,
            'longitude': station['geom'].x
        })
    
    context = {'stations': stations}
    template = loader.get_template('stations/index.html')
    return HttpResponse(template.render(context, request))


def get_all_stations_json(request):
    stations = list()
    for station in EnciclaStation.objects.values():
        stations.append({
            'name': station['name'],
            'address': station['address'],
            'capacity': station['capacity'],
            'status': station['status'],
            'latitude': station['geom'].y,
            'longitude': station['geom'].x
        })
    return JsonResponse(list(stations), safe=False)
