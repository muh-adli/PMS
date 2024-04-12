## Django core
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse
from django.contrib.gis.db.models.functions import Transform
from django.contrib.auth.decorators import login_required


## Models and Serializers Import
from .models import *

## Library
from datetime import datetime

### Create your views here.

@login_required()
def MapHectare(request):
    return render(request, "map/Hectare.html")

@login_required()
def MapBlock(request):
    return render(request, "map/block.html")

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

    qs = Afdeling.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Afdeling_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("AfdelingBoundary qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Afdeling_qs, content_type='json')

def JembatanData(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = Jembatan.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Jembatan_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("JembatanData qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Jembatan_qs, content_type='json')

def PatokData(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = Patokhgu.objects.annotate(
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
def BlockBoundary(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = Block.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Block_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("BlockBoundary qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Block_qs, content_type='json')