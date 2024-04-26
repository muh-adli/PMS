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

def ApiBlockBoundary(request):
    now = datetime.now()
    # print("start: ", str(now))

    qs = Block.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Block_qs = serialize('geojson', qs)
    end = datetime.now()
    # print("end: ", str(end))
    delta = end - now
    print("ApiBlockBoundary qs: ", round(delta.total_seconds(), 3),'S')
    # return render(request, "html/map.html", {'Building_qs':Building_qs})
    return HttpResponse(Block_qs, content_type='json')