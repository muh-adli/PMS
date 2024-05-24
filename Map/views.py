## Django core
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.contrib.gis.db.models.functions import Transform
from django.contrib.auth.decorators import login_required
from django.db.models import F, Case, When, Value, CharField

from rest_framework import generics
from rest_framework_gis.serializers import GeoFeatureModelSerializer


## Models and Serializers Import
from .models import *

## Library
from datetime import datetime
import json
### Create your views here.

@login_required()
def MapHectare(request):
    return render(request, "map/static_map.html")

## API GeoJSON
@login_required()
def HGUBoundary(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = Hgu.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    HGU_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("HGUBoundary qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(HGU_qs, content_type='json')

@login_required()
def AfdelingBoundary(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = HguAfdeling.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Afdeling_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("Afdeling qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Afdeling_qs, content_type='json')

@login_required()
def JembatanData(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = HguJembatan.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Jembatan_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("JembatanData qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Jembatan_qs, content_type='json')

@login_required()
def DumpData(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = TankosDumpdata.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Patok_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("Dumpdata qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Patok_qs, content_type='json')

@login_required()
def PatokData(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = HguPatok.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Patok_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("PatokData qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Patok_qs, content_type='json')

@login_required()
def PlantedData(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = HguPlanted.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Planted_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("PlantedData qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Planted_qs, content_type='json')

@login_required()
def BlockBoundary(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = HguBlock.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Block_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("BlockBoundary qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Block_qs, content_type='json')

@login_required()
def TankosDumpStatus(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = TankosDumpdata.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Block_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("BlockBoundary qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Block_qs, content_type='json')

@login_required()
def RoadData(request): # TODO: FIXING API
    now = datetime.now()

    qs = HguJalan.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()
    print(qs)
    # end1 = datetime.now()

    road_qs = serialize('geojson', qs, geometry_field='geometry')
    # end2 = datetime.now()

    # Calculate execution time
    end = datetime.now()
    delta = end - now

    # Print execution time for debugging (optional)
    print("Road serialize: ", round(delta.total_seconds(), 3), 'S')
    return HttpResponse(road_qs, content_type='application/json')

@login_required()
def DumpDataV2(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = TankosDumpApi.objects.all()

    Patok_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("Dumpdata qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Patok_qs, content_type='json')

@login_required()
def AplDataV2(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = TankosAplApi.objects.all()

    Patok_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("Apldata qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Patok_qs, content_type='json')

@login_required()
def PlantedDataV2(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = TankosAplApi.objects.all()

    Patok_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("Apldata qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Patok_qs, content_type='json')

@login_required()
def PlantedDataV2(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = HguplantedView.objects.all()

    Patok_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("Planted qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Patok_qs, content_type='json')

@login_required()
def BlockDataV2(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = HgublockView.objects.all()

    Patok_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("Block qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Patok_qs, content_type='json')