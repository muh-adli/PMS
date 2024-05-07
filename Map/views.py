## Django core
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse
from django.contrib.gis.db.models.functions import Transform
from django.contrib.auth.decorators import login_required
from django.db.models import F, Case, When, Value, CharField


## Models and Serializers Import
from .models import *

## Library
from datetime import datetime

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

# @login_required()
# def JangkosData(request):
#     qs = Block.objects.annotate(
#             jangkos = Case(
#                         When(gid__jangkos_gid__isnull=False, then=Value('Data Available')),
#                         default=Value('No Data Available'),
#                         output_field=CharField()
#                         )
#         ).order_by('jangkos')
#     for block in qs:
#         print(f"GID: {block.gid}, Object ID: {block.objectid}, AFD Name: {block.afd_name}, Block Name: {block.block_name}, HA: {block.ha}, Estate: {block.estate}, Jangkos Data Status: {block.jangkos}")
#     return HttpResponse(qs, content_type='json')

@login_required()
def TankosDump(request):
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

