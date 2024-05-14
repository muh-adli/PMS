from django.shortcuts import render
from django.contrib import messages
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.contrib.gis.db.models.functions import Transform
from django.contrib.auth import authenticate

import json


## Models and Serializers Import
from .models import *
from Map.models import *

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
    
def ApiPatokData(request):
    query = request.GET.get('q')
    if query:
        patok_qs = HguPatok.objects.filter(no_patok__icontains=query).order_by('no_patok')

        ## Checking available data
        if patok_qs is None:
            messages.warning("Data isn't available")

    else:
        ## Data collecting and cleansing from database
        patok_qs = HguPatok.objects.all()
        # patok_pagi = PatokTable(patok_qs)
        # patok_pagi.paginate(page=request.GET.get("page", 1), per_page=15)

        ## Context dictionary for passing data

    print("Request patok data from apps")

    json = {}
    json['status'] = "200"
    json['error'] = False
    json['data'] = []
    for data in patok_qs:
        append_data = {
            'no_patok' : data.no_patok,
            'afd_name' : data.afd_name,
            'block_name' : data.block_name,
            'longtitude' : data.longitude,
            'latitude' : data.latitude,
            'period' : data.periode,
            'status' : data.status,
            'id' : data.objectid
        }
        json['data'].append(append_data)
    
    return JsonResponse(json, safe=False)