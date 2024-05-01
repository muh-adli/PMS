## Django build-in fuctions
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count, Sum, Q
from django.contrib.gis.db.models.functions import Transform


# Models and forms
from .models import *
from .forms import *
from .tables import *
from Map.models import *

## Library
import pandas as pd
from datetime import datetime
import io

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
    return render(request, "dashboard/static_center_dashboard.html", context)

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
    return render(request, "dashboard/static_hectarestatement_dashboard.html", context)

@login_required(login_url="")
def Tankos(request):
    Title = 'Dashboard - Tankos'

    ## Querying data
    Tankos_qs = TankosSummary.objects.values(
        'afdeling',
        'block',
        'area',
        'date',
        'date_delta',
        'status',
        )

    ## Table data
    TableData = Tankos_qs.order_by('afdeling','block')[:10]
    # print(TableData)

    ## Context
    context = {
        'TableData' : TableData,
        'Title':Title
    }
    return render(request, "dashboard/static_tankos_dashboard.html", context)

def AplPokokTable(request):
    Title = 'Dashboard - pokok'
    query = request.GET.get('q')
    if query:
        pokok_qs = TankosAplpokok.objects.filter(block=query).order_by('-date')

        ## Checking available data
        if pokok_qs is None:
            messages.warning("Data isn't available")
            return redirect('AplPokokTable')

        else:
            ## Context dictionary for passing data
            context = {
                'Title': Title,
                'TableData' : pokok_qs,
            }

    else:
        ## Data collecting and cleansing from database
        pokok_qs = TankosAplpokok.objects.all().order_by('-date') #TODO: Paginate table to 15 item

        ## Context dictionary for passing data
        context = {
            'Title': Title,
            'TableData' : pokok_qs,
        }
    return render(request, "dashboard/static_tankos_tabledata.html", context)

def AplTonaseTable(request):
    Title = 'Dashboard - tonase'
    query = request.GET.get('q')
    if query:
        tonase_qs = TankosApltonase.objects.filter(block=query).order_by('-date')

        ## Checking available data
        if tonase_qs is None:
            messages.warning("Data isn't available")
            return redirect('AplTonaseTable')

        else:
            ## Context dictionary for passing data
            context = {
                'Title': Title,
                'TableData' : tonase_qs,
            }

    else:
        ## Data collecting and cleansing from database
        tonase_qs = TankosApltonase.objects.all().order_by('-date') #TODO: Paginate table to 15 item

        ## Context dictionary for passing data
        context = {
            'Title': Title,
            'TableData' : tonase_qs,
        }
    return render(request, "dashboard/static_tankos_tabledata.html", context)

def DumpTable(request):
    Title = 'Dashboard - dump'
    query = request.GET.get('q')
    if query:
        dump_qs = TankosDumpdata.objects.filter(location=query).order_by('-dump_date')

        ## Checking available data
        if dump_qs is None:
            messages.warning("Data isn't available")
            return redirect('DumpTable')

        else:
            ## Context dictionary for passing data
            context = {
                'Title': Title,
                'TableData' : dump_qs,
            }

    else:
        ## Data collecting and cleansing from database
        dump_qs = TankosDumpdata.objects.all().order_by('-dump_date') #TODO: Paginate table to 15 item

        ## Context dictionary for passing data
        context = {
            'Title': Title,
            'TableData' : dump_qs,
        }
    return render(request, "dashboard/static_tankos_tabledata.html", context)


@login_required(login_url="")
def TankosTable(request):
    Title = 'Table - Tankos'
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
    return render(request, "dashboard/static_tankos_table.html", context)

@login_required(login_url="")
def TankosEdit(request, gid):

    # Title
    Title = 'Edit Tankos'
    geomid = gid

    #  Query
    Block_qs = HguPlanted.objects.values(
            'afd_name','block_name','ha'
            ).annotate(
                geometry=Transform('geom', 4326)
            ).get(gid=gid)
    print(Block_qs)

    # Tankos_qs = get_object_or_404(Tankos, id=gid)
    # print(Tankos_qs)

    # Wrangling and Cleaning
    data = {
        'afd_name' : Block_qs['afd_name'],
        'block_name' : Block_qs['block_name'],
        'area' : str(round(Block_qs['ha'], 2)) + ' Ha'
    }
    # print(data)
    # form = EditTankosForm(instance=Tankos_qs)
    FormAdditional = EditTankosFormAdd(initial=data)

    # Editing data
    if request.method == 'POST' :
        # print(request.POST)
        form = EditTankosForm(
                                request.POST,
                                # instance=Tankos_qs
                            )
        if form.is_valid():
            form.save()
            print("Blok updated successfully.")
            messages.success(request, 'Blok updated successfully.')
            return redirect('TankosTable')
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
    return render(request,'dashboard/static_tankos_table_edit.html', context )

@login_required(login_url="")
def Pupuk(request):
    Title = 'Dashboard - Pupuk'
    # ## Data collecting and cleansing from database
    # pupuk_qs =

    ## Context
    context = {
        'Title':Title,
    }
    return render(request, "dashboard/static_pupuk_dashboard.html", context)

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
    return render(request, "dashboard/static_patok_dashboard.html", context)

def PatokTable(request):
    Title = 'Dashboard - Patok'
    query = request.GET.get('q')
    if query:
        patok_qs = HguPatok.objects.filter(no_patok__icontains=query).order_by('no_patok')

        ## Checking available data
        if patok_qs is None:
            messages.warning("Data isn't available")
            return redirect('PatokTable')

        else:
            ## Context dictionary for passing data
            context = {
                'Title': Title,
                'TableData' : patok_qs,
            }

    else:
        ## Data collecting and cleansing from database
        patok_qs = HguPatok.objects.all()
        # patok_pagi = PatokTable(patok_qs)
        # patok_pagi.paginate(page=request.GET.get("page", 1), per_page=15)

        ## Context dictionary for passing data
        context = {
            'Title': Title,
            'TableData' : patok_qs,
            # 'patok_pagi' : patok_pagi
        }
    return render(request, "dashboard/static_patok_table.html", context)

def PatokExtract(request):

    date = str(datetime.now().strftime('%d-%m-%Y'))
    print(date)
    ## Data collecting and cleansing from database
    patok_qs = HguPatok.objects.values(
        'kode',
        'afd_name',
        'block_name',
        'no_patok',
        'periode',
        'status',
        'x',
        'y',
        'longitude',
        'latitude',
    ).order_by('no_patok')
    data = pd.DataFrame(patok_qs)
    data = data.rename(columns={
    'kode':'Kode',
    'afdeling': 'Afdeling',
    'block_name': 'Block',
    'no_patok': 'Patok',
    'periode':'Periode',
    'status':'Status',
    'x':'Koordinat X',
    'y':'Koordinat Y',
    'longitude':'Longitude',
    'latitude':'Latitude',
    })
    data = data.reindex(columns=[
    'Kode',
    'Afdeling',
    'Block',
    'Patok',
    'Periode',
    'Status',
    'Koordinat X',
    'Koordinat Y',
    'Longitude',
    'Latitude',
    ])
    # Create BytesIO buffer to write the Excel file
    output = io.BytesIO()
    data.to_excel(output, index=False)

    # Create an HTTP response with the Excel file
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={date}_Patok.xlsx'
    return response

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
    return render(request, "dashboard/static_patok_table_edit.html", context)

@login_required(login_url="")
def ExtJangkos(request):
    return render(request, "dashboard/asd.html")