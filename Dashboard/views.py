## Django build-in fuctions
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count, Sum
from django.contrib.gis.db.models.functions import Transform
from django.contrib import messages
from django.core.serializers import serialize
from django.http import JsonResponse

# Models and forms
from .models import *
from .forms import *
from .tables import *
from Map.models import *

## Library
from django_tables2.tables import Paginator
import django_tables2 as tables
from plotly.subplots import make_subplots
from plotly.offline import plot
import plotly.graph_objects as go

# Create your views here.
@login_required(login_url="")
def HomePage(request):
    Title = 'HomePage'
    context = {'Title':Title}
    return render(request, "static_home.html",context)

@login_required(login_url="")
def center(request):
    Title = 'Dashboard - Center'

    context = {
        'Title': Title,
    }
    return render(request, "dashboard/static_dashboard_center.html", context)

@login_required(login_url="")
def hectare(request):
    Title = 'Dashboard - Hectare Statement'
    Planted_qs = HguPlanted.objects.aggregate(total_ha=Sum('ha'))
    HGU_qs = Hgu.objects.aggregate(total_ha=Sum('ha'))
    
    tot_Planted = round(Planted_qs['total_ha'], 2)
    tot_HGU = round(HGU_qs['total_ha'], 2)

    context = {
        'Title': Title,
        'Planted': tot_Planted,
        'HGU': tot_HGU,
    }
    return render(request, "dashboard/static_dashboard_hectarestatement.html", context)

@login_required(login_url="")
def jangkos(request):
    Title = 'Dashboard - Jangkos'

    ## Querying data
    jangkos_qs = TankosSummary.objects.values(
        'afdeling',
        'block',
        'area',
        'date',
        'date_delta',
        'status',
        )

    afdeling = models.CharField(max_length=5, blank=True, null=True)
    block = models.CharField(max_length=5, blank=True, null=True)
    area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    date_delta = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    pokok = models.IntegerField(blank=True, null=True)
    tonase = models.FloatField(blank=True, null=True)

    ## Table data
    TableData = jangkos_qs.order_by('afdeling','block')[:10]
    # print(TableData)

    ## Context
    context = {
        'TableData' : TableData,
        'Title':Title
    }
    return render(request, "dashboard/static_dashboard_jangkos.html", context)

@login_required(login_url="")
def JangkosTable(request):
    Title = 'Table - Jangkos'
    TableData = TankosSummary.objects.values(
        'afdeling',
        'block',
        'area',
        'date',
        'date_delta',
        'status',
        )
    
    # Download Content

    context = {
        'TableData' : TableData,
        'Title':Title
    }
    return render(request, "dashboard/static_table_jangkos.html", context)

@login_required(login_url="")
def JangkosEdit(request, gid):

    # Title
    Title = 'Edit Jangkos'
    geomid = gid

    #  Query
    Block_qs = HguPlanted.objects.values(
            'afd_name','block_name','ha'
            ).annotate(
                geometry=Transform('geom', 4326)
            ).get(gid=gid)
    print(Block_qs)

    # Jangkos_qs = get_object_or_404(Jangkos, id=gid)
    # print(Jangkos_qs)

    # Wrangling and Cleaning
    data = {
        'afd_name' : Block_qs['afd_name'],
        'block_name' : Block_qs['block_name'],
        'area' : str(round(Block_qs['ha'], 2)) + ' Ha'
    }
    # print(data)
    # form = EditJangkosForm(instance=Jangkos_qs)
    FormAdditional = EditJangkosFormAdd(initial=data)

    # Editing data
    if request.method == 'POST' :
        # print(request.POST)
        form = EditJangkosForm(
                                request.POST,
                                # instance=Jangkos_qs
                            )
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

@login_required(login_url="")
def pupuk(request):
    Title = 'Dashboard - Pupuk'
    # ## Data collecting and cleansing from database
    # pupuk_qs =

    ## Context
    context = {
        'Title':Title,
    }
    return render(request, "dashboard/static_dashboard_pupuk.html", context)

@login_required(login_url="")
def Patok(request):
    Title = 'Dashboard - Patok'

    ## Data collecting and cleansing from database
    patok_qs = HguPatok.objects.all()

    ## data wrangling for Graph
    list_key = []
    list_value = []
    periode_counts = {
            'Q1': 0,
            'Q2': 0,
            'Q3': 0,
            'Q4': 0,
            'N/A': 0
        }

    for patok in patok_qs:
        periode = patok.periode # get periode value in patok for loop
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
    # print(periode_counts)

    for key, value in periode_counts.items():
        list_key.append(key)
        list_value.append(value)

    # print(list_key)
    # print(list_value)

    ## Table
    patokTable = patok_qs[:5]
    print(patokTable)
    table = PatokDashboardTable(patokTable)

    ## Context dictionary for passing data
    context = {
        'Title' : Title,
        'periode' : list_key,
        'count' : list_value,
        'table' : table,
        }
    return render(request, "dashboard/static_dashboard_patok.html", context)


def PatokTable(request):
    Title = 'Dashboard - Patok'
    ## Data collecting and cleansing from database
    patok_qs = HguPatok.objects.all()
    # patok_pagi = PatokTable(patok_qs)
    # patok_pagi.paginate(page=request.GET.get("page", 1), per_page=15)

    # Context dictionary for passing data
    context = {
        'Title': Title,
        'TableData' : patok_qs,
        # 'patok_pagi' : patok_pagi
    }
    return render(request, "dashboard/static_table_patok.html", context)

@login_required(login_url="")
def PatokEdit(request, gid):

    # Title
    Title = 'Edit Jangkos'
    geomid = gid

    patok_qs = get_object_or_404(HguPatok, gid=gid)
    print(patok_qs)

    # Wrangling and Cleaning

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
    return render(request, "dashboard/static_table_edit_patok.html", context)

@login_required(login_url="")
def ExtJangkos(request):
    return render(request, "dashboard/asd.html")