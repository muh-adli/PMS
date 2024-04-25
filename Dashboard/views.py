## Django build-in fuctions
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count
from django.contrib.gis.db.models.functions import Transform
from django.contrib import messages
from django.core.serializers import serialize
import json
from django.http import JsonResponse

# Models and forms
from .models import *
from .forms import *
from Map.models import *

## Library
from plotly.subplots import make_subplots
from plotly.offline import plot
import plotly.graph_objects as go

# Create your views here.
@login_required(login_url="/login")
def HomePage(request):
    Title = 'HomePage'
    context = {'Title':Title}
    return render(request, "static_home.html",context)

@login_required(login_url="/login")
def center(request):
    Title = 'Dashboard - Center'

    context = {
        'Title': Title,
    }
    return render(request, "dashboard/static_dashboard_center.html", context)

@login_required(login_url="/login")
def jangkos(request):
    Title = 'Dashboard - Jangkos'

    ## Querying data
    block_qs = Block.objects.annotate(
        geometry=Transform('geom', 4326)
    ).values('gid', 'objectid', 'afd_name', 'block_name', 'geometry', 'ha', 'estate')
    jangkos_qs = Jangkos.objects.values('afd_name','block_name','dumps','aplikasi')

    ## Table data
    TableData = jangkos_qs.order_by('dumps','aplikasi')[:10]
    # print(TableData)

    ## Context
    context = {
        'TableData' : TableData,
        'Title':Title
    }
    return render(request, "dashboard/static_dashboard_jangkos.html", context)

@login_required(login_url="/login")
def JangkosTable(request):
    Title = 'Table - Jangkos'
    TableData = Jangkos.objects.values(
        'afd_name','block_name','dumps','aplikasi','selisih','gid'
        )
    
    # Download Content

    context = {
        'TableData' : TableData,
        'Title':Title
    }
    return render(request, "dashboard/static_table_jangkos.html", context)

@login_required(login_url="/login")
def JangkosEdit(request, gid):

    # Title
    Title = 'Edit Jangkos'
    geomid = gid

    #  Query
    Block_qs = Block.objects.values(
            'afd_name','block_name','ha'
            ).annotate(
                geometry=Transform('geom', 4326)
            ).get(gid=gid)
    print(Block_qs)

    Jangkos_qs = get_object_or_404(Jangkos, id=gid)
    # print(Jangkos_qs)

    # Wrangling and Cleaning
    data = {
        'afd_name' : Block_qs['afd_name'],
        'block_name' : Block_qs['block_name'],
        'area' : str(round(Block_qs['ha'], 2)) + ' Ha'
    }
    # print(data)
    form = EditJangkosForm(instance=Jangkos_qs)
    FormAdditional = EditJangkosFormAdd(initial=data)

    # Editing data
    if request.method == 'POST' :
        # print(request.POST)
        form = EditJangkosForm(request.POST, instance=Jangkos_qs)
        if form.is_valid():
            form.save()
            print("Blok updated successfully.")
            messages.success(request, 'Blok updated successfully.')
            return redirect('JangkosTable')
        else:
            print(form.errors)
            print("Error saving data.")
            messages.error(request, 'Error saving data.')
    else:
        messages.error(request, 'Error loading data.')

    context={
        'formadd':FormAdditional,
        'form':form,
        'Title':Title,
        'geomid':geomid,
    }
    return render(request,'dashboard/static_table_edit_jangkos.html', context )

@login_required(login_url="/login")
def pupuk(request):
    Title = 'Dashboard - Pupuk'
    # ## Data collecting and cleansing from database
    # pupuk_qs = 

    ## Context
    context = {
        'Title':Title,
        
    }
    return render(request, "dashboard/dashboard_jangkos.html", context)

@login_required(login_url="/login")
def Monitoring(request):
    Title = 'Dashboard - Monitoring'
    ## Data collecting and cleansing from database
    
    MR_qs = Road.objects.filter(rd_sym="MR")
    print(MR_qs.count())
    CR_qs = Road.objects.filter(rd_sym="CR")
    print(CR_qs.count())
    CT_qs = Road.objects.filter(rd_sym="CT")
    print(CT_qs.count())

    ## Visualization
    ## Color pallete
    color3 = ['#003f5c','#bc5090','#ffa600']
    color4 = ['#003f5c','#7a5195','#ef5675','#ffa600']
    color5 = ['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']
    color6 = ['#003f5c','#444e86','#955196','#dd5182','#ff6e54','#ffa600']
    color7 = ['#003f5c','#374c80','#7a5195','#bc5090','#ef5675','#ff764a','#ffa600']
    color8 = ['#003f5c','#2f4b7c','#665191','#a05195','#d45087','#f95d6a','#ff7c43','#ffa600']

    # Context dictionary for passing data
    context = {
        'Title': Title,

    }
    return render(request, "dashboard/static_dashboard_monitoring.html", context)

@login_required(login_url="/login")
def PatokTable(request):
    Title = 'Dashboard - Patok'
    ## Data collecting and cleansing from database
    patok_qs = MonitoringPatokhgu.objects.all().order_by('no_patok')

    ## Visualization
    ## Color pallete
    color3 = ['#003f5c','#bc5090','#ffa600']
    color4 = ['#003f5c','#7a5195','#ef5675','#ffa600']
    color5 = ['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']
    color6 = ['#003f5c','#444e86','#955196','#dd5182','#ff6e54','#ffa600']
    color7 = ['#003f5c','#374c80','#7a5195','#bc5090','#ef5675','#ff764a','#ffa600']
    color8 = ['#003f5c','#2f4b7c','#665191','#a05195','#d45087','#f95d6a','#ff7c43','#ffa600']

    # Context dictionary for passing data
    context = {
        'Title': Title,
        'TableData' : patok_qs
    }
    return render(request, "dashboard/static_table_patok.html", context)

@login_required(login_url="/login")
def PatokEdit(request, gid):

    # Title
    Title = 'Edit Jangkos'
    geomid = gid

    patok_qs = get_object_or_404(MonitoringPatokhgu, gid=gid)
    # print(Jangkos_qs)

    # Wrangling and Cleaning

    # print(data)
    form = EditPatokForm(instance=patok_qs)

    # Editing data
    if request.method == 'POST' :
        # print(request.POST)
        form = EditPatokForm(request.POST, instance=patok_qs)
        if form.is_valid():
            form.save()
            print("Blok updated successfully.")
            messages.success(request, 'Blok updated successfully.')
            return redirect('JangkosTable')
        else:
            print(form.errors)
            print("Error saving data.")
            messages.error(request, 'Error saving data.')
    else:
        messages.error(request, 'Error loading data.')

    context={
        'form':form,
        'Title':Title,
        'geomid':geomid,
    }
    return render(request, "dashboard/asd.html", context)

@login_required(login_url="/login")
def ExtJangkos(request):
    return render(request, "dashboard/asd.html")