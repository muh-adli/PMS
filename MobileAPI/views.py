from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.contrib.gis.db.models.functions import Transform
from django.contrib.auth import authenticate


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

def ApiLoginRequest(request):
    if request.method == "GET" and 'username' in request.GET and 'password' in request.GET:
        print("Request login from apps")
        username = request.GET['username']
        password = request.GET['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("BERHASIL LOGIN")
            return JsonResponse(
                {
                    'status' : '200',
                    'message' : 'Login success',
                }
            )
        else:
            print("USER GA NEMU")
            return JsonResponse(
                {
                    'status' : '201',
                    'message' : 'User not found',
                }
            )
    else:
        return JsonResponse(
                {
                    'status' : '201',
                    'message' : 'Request error',
                }
            )