from django.shortcuts import render
from django.contrib import messages
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.contrib.gis.db.models.functions import Transform
from django.contrib.auth import authenticate
from django.db.models import F, Count, Sum, Q, Min, Max

import json


## Models and Serializers Import
from .models import *
from Map.models import *
from Dashboard.models import *

## Library
from datetime import datetime, timedelta

def ApiBlockBoundary(request):
    print("Request block boundary from apps")

    qs = HguBlock.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Block_qs = serialize('geojson', qs)
    Block_qs = json.loads(Block_qs)

    return JsonResponse(Block_qs, safe=False)

def ApiDumpBoundary(request):
    print("Request dump boundary from apps")

    qs = TankosDumpdata.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Patok_qs = serialize('geojson', qs)
    Patok_qs = json.loads(Patok_qs)

    return JsonResponse(Patok_qs, safe=False)

def ApiHguBoundary(request):
    print("Request hgu boundary from apps")

    qs = Hgu.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    HGU_qs = serialize('geojson', qs)
    HGU_qs = json.loads(HGU_qs)

    return JsonResponse(HGU_qs, safe=False)

def ApiAfdelingBoundary(request):
    print("Request afdeling boundary form apps")

    qs = HguAfdeling.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Afdeling_qs = serialize('geojson', qs)
    Afdeling_qs = json.loads(Afdeling_qs)

    return JsonResponse(Afdeling_qs, safe=False)

def ApiPlantedBoundary(request):
    print("Request planted boundary form apps")
    
    qs = HguPlanted.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Planted_qs = serialize('geojson', qs)
    Planted_qs = json.loads(Planted_qs)

    return JsonResponse(Planted_qs, safe=False)

def ApiRoadBoundary(request):
    print("Request road boundary form apps")
    
    qs = HguJalan.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    road_qs = serialize('geojson', qs)
    road_qs = json.loads(road_qs)

    return JsonResponse(road_qs, safe=False)

def ApiBridgeBoundary(request):
    print("Request road boundary form apps")
    
    qs = HguJembatan.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Jembatan_qs = serialize('geojson', qs)
    Jembatan_qs = json.loads(Jembatan_qs)

    return JsonResponse(Jembatan_qs, safe=False)

def ApiPatokBoundary(request):
    print("Request road boundary form apps")
    
    qs = HguPatok.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Patok_qs = serialize('geojson', qs)
    Patok_qs = json.loads(Patok_qs)

    return JsonResponse(Patok_qs, safe=False)

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
    print("Request patok data from apps")
    query = request.GET.get('q')
    if query:
        patok_qs = HguPatok.objects.filter(no_patok__icontains=query).order_by('no_patok')

        if patok_qs is None:
            messages.warning("Data isn't available")

            json = {}
            json['status'] = "201"
            json['error'] = True

            return JsonResponse(json, safe=False)
    else:
        patok_qs = HguPatok.objects.all()

    json = {}
    json['status'] = "200"
    json['error'] = False
    json['data'] = []

    periode_counts = {
            'Q1': 0,
            'Q2': 0,
            'Q3': 0,
            'Q4': 0,
            'N/A': 0
        }
    
    for data in patok_qs:
        append_data = {
            'no_patok' : data.no_patok,
            'afd_name' : data.afd_name,
            'block_name' : data.block_name,
            'longtitude' : data.longitude,
            'latitude' : data.latitude,
            'period' : data.periode,
            'status' : data.status,
            'id' : data.gid
        }
        json['data'].append(append_data)

        periode = data.periode
        if periode == 'Q1':
            periode_counts['Q1'] += 1
        elif periode == 'Q2':
            periode_counts['Q2'] += 1
        elif periode == 'Q3':
            periode_counts['Q3'] += 1
        elif periode == 'Q4':
            periode_counts['Q4'] += 1
        else:
            periode_counts['N/A'] += 1


    json['chart'] = periode_counts
    
    return JsonResponse(json, safe=False)

def ApiPlantedData(request):
    print("Request planted data from apps")
    planted_qs = HguPlanted.objects.all()

    json = {}
    json['status'] = "200"
    json['error'] = False
    json['data'] = []

    for data in planted_qs:
        append_data = {
            'id' : data.gid,
            'afd_name' : data.afd_name,
            'block_name' : data.block_name,
            'block_sap' : data.block_sap,
            'ha' : data.ha,
            'year' : data.tahun,
            'level1' : data.level_1,
            'level2' : data.level_2,
            'status' : data.status,
        }

        json['data'].append(append_data)

        json['luas'] = {
            'hgu' : "1000",
            'planted' : "1000",
        }

    return JsonResponse(json, safe=False)

def ApiDumpData(request):
    print("Request dump data from apps")
    query = request.GET.get('q')
    if query:
        dump_qs = TankosDumpdata.objects.filter(location__contains=query).order_by('dump_date')

        if dump_qs is None:
            messages.warning("Data isn't available")

            return JsonResponse(json, safe=False)
    else:
        dump_qs = TankosDumpdata.objects.all().order_by('dump_date')

    json = {}
    json['status'] = "200"
    json['error'] = False
    json['data'] = []

    for data in dump_qs:
        append_data = {
            'id' : data.gid,
            'afdeling' : data.afdeling,
            'block' : data.block,
            'location' : data.location,
            'dump_date' : data.dump_date,
        }

        json['data'].append(append_data)

    return JsonResponse(json, safe=False)

def ApiTankosChart(request):
    print("Request tankos chart data from apps")

    pokok_count_by_date = TankosAplpokok.objects.values('date').annotate(count=Count('date'))
    tonase_count_by_date = TankosApltonase.objects.values('date').annotate(count=Count('date'))

    pokok_data = TankosAplpokok.objects.all()
    tonase_data = TankosApltonase.objects.all()
    dump_data = TankosDumpdata.objects.all()

    # Get minimum and maximum dates
    pokok_min_date = pokok_data.aggregate(min_date=Min('date'))['min_date']
    pokok_max_date = pokok_data.aggregate(max_date=Max('date'))['max_date']

    tonase_min_date = tonase_data.aggregate(min_date=Min('date'))['min_date']
    tonase_max_date = tonase_data.aggregate(max_date=Max('date'))['max_date']
    
    dump_min_date = dump_data.aggregate(min_date=Min('dump_date'))['min_date']
    dump_max_date = dump_data.aggregate(max_date=Max('dump_date'))['max_date']

    min_date = min(pokok_min_date, tonase_min_date, dump_min_date)
    max_date = max(pokok_max_date, tonase_max_date, dump_max_date)

    # Generate all dates between min and max date
    all_dates = [min_date + timedelta(days=x) for x in range((max_date - min_date).days + 1)]
    # print(all_dates)
    all_date = [(min_date + timedelta(days=x)).strftime("%Y-%m-%d") for x in range((max_date - min_date).days + 1)]
    # print(all_date)

    # Aggregate data by date
    pokok_count_by_date = pokok_data.values('date').annotate(count=Count('date'))
    tonase_count_by_date = tonase_data.values('date').annotate(count=Count('date'))
    dump_count_by_date = dump_data.values('dump_date').annotate(count=Count('dump_date'))

    # Initialize dictionaries to hold counts for each date
    pokok_counts_dict = {entry['date']: entry['count'] for entry in pokok_count_by_date}
    tonase_counts_dict = {entry['date']: entry['count'] for entry in tonase_count_by_date}
    dump_counts_dict = {entry['dump_date']: entry['count'] for entry in dump_count_by_date}


    # Fill in counts for all dates, including missing ones
    pokok_counts = [pokok_counts_dict.get(date, 0) for date in all_dates]
    tonase_counts = [tonase_counts_dict.get(date, 0) for date in all_dates]
    dump_counts = [dump_counts_dict.get(date, 0) for date in all_dates]

    json = {}
    json['status'] = "200"
    json['error'] = False
    json['chart'] = {
        'date' : all_date,
        'pokok' : pokok_counts,
        'tonase' : tonase_counts,
        'dump' : dump_counts,
    }

    return JsonResponse(json, safe=False)

def ApiAplData(request):
    query = request.GET.get('q')

    if query:
        sum_qs = TankosAplsummary.objects.filter(block__contains=query)

        if sum_qs is None:
            messages.warning("Data isn't available")

    else:
        sum_qs = TankosAplsummary.objects.all()

    for data in sum_qs:
        print(data.block)
    ##return JsonResponse(sum_qs, safe=False)

def ApiSaveDump(request, gid):
    if request.method == "GET" and 'date' in request.GET:
        qs = TankosDumpdata.objects.filter(pk=gid).update(dump_date=request.GET['date'])

        if qs:
            print("Update tankos from apps success")
            return JsonResponse(
                {
                    'status' : '200',
                    'message' : 'Update Success',
                }
            )
        else:
            print("Update tankos from apps failed")
            return JsonResponse(
                {
                    'status' : '201',
                    'message' : 'Update Failed',
                }
            )
    else:
        print("Update tankos from apps error")
        return JsonResponse(
                {
                    'status' : '201',
                    'message' : 'Request error',
                }
            )
    
def ApiSavePatok(request, gid):
    if request.method == "GET" and 'period' in request.GET:
        qs = HguPatok.objects.filter(pk=gid).update(periode=request.GET['period'])

        if qs:
            print("Update patok from apps success")
            return JsonResponse(
                {
                    'status' : '200',
                    'message' : 'Update Success',
                }
            )
        else:
            print("Update patok from apps failed")
            return JsonResponse(
                {
                    'status' : '201',
                    'message' : 'Update Failed',
                }
            )
    else:
        print("Update patok from apps error")
        return JsonResponse(
                {
                    'status' : '201',
                    'message' : 'Request error',
                }
            )