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
    now = datetime.now()

    qs = HguBlock.objects.annotate(
        geometry=Transform('geom', 4326),
    ).all()

    Block_qs = serialize('geojson', qs)
    Block_qs = json.loads(Block_qs)
    end = datetime.now()
    delta = end - now

    print("ApiBlockBoundary qs: ", round(delta.total_seconds(), 3),'S')
    
    ##return HttpResponse(Block_qs, content_type='json')
    return JsonResponse(Block_qs, safe=False)

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

            json = {}
            json['status'] = "201"
            json['error'] = True

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

    json['chart'] = {
        'date' : all_date,
        'pokok' : pokok_counts,
        'tonase' : tonase_counts,
        'dump' : dump_counts,
    }

    return JsonResponse(json, safe=False)