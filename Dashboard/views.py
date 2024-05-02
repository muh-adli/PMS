## Django build-in fuctions
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count, Sum, Q, Min, Max
from django.contrib.gis.db.models.functions import Transform


# Models and forms
from .models import *
from .forms import *
from .tables import *
from Map.models import *

## Library
from datetime import timedelta
from django.utils import timezone
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
from plotly.offline import plot
import io
import time

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

    pokok_count_by_date = TankosAplpokok.objects.values('date').annotate(count=Count('date'))
    tonase_count_by_date = TankosApltonase.objects.values('date').annotate(count=Count('date'))

    # Query data from TankosAplpokok model
    pokok_data = TankosAplpokok.objects.all()

    # Query data from TankosApltonase model
    tonase_data = TankosApltonase.objects.all()

    # Get minimum and maximum dates
    pokok_min_date = pokok_data.aggregate(min_date=Min('date'))['min_date']
    pokok_max_date = pokok_data.aggregate(max_date=Max('date'))['max_date']

    tonase_min_date = tonase_data.aggregate(min_date=Min('date'))['min_date']
    tonase_max_date = tonase_data.aggregate(max_date=Max('date'))['max_date']

    min_date = min(pokok_min_date, tonase_min_date)
    max_date = max(pokok_max_date, tonase_max_date)

    # Generate all dates between min and max date
    all_dates = [min_date + timedelta(days=x) for x in range((max_date - min_date).days + 1)]
    print(all_dates)
    all_date = [(min_date + timedelta(days=x)).strftime("%Y-%m-%d") for x in range((max_date - min_date).days + 1)]
    print(all_date)

    # Aggregate data by date
    pokok_count_by_date = pokok_data.values('date').annotate(count=Count('date'))
    tonase_count_by_date = tonase_data.values('date').annotate(count=Count('date'))

    # Initialize dictionaries to hold counts for each date
    pokok_counts_dict = {entry['date']: entry['count'] for entry in pokok_count_by_date}
    tonase_counts_dict = {entry['date']: entry['count'] for entry in tonase_count_by_date}

    # Fill in counts for all dates, including missing ones
    pokok_counts = [pokok_counts_dict.get(date, 0) for date in all_dates]
    tonase_counts = [tonase_counts_dict.get(date, 0) for date in all_dates]
    print(pokok_counts)
    print(tonase_counts)

    ## Context
    context = {
        'Title':Title,
        'all_dates': all_date,
        'pokok_counts':pokok_counts,
        'tonase_counts':tonase_counts,
    }
    return render(request, "dashboard/static_tankos_dashboard.html", context)


## Aplikasi pokok and tonase
def AplSummary(request):
    Title = 'Dashboard - Aplikasi'
    query = request.GET.get('q')

    if query:
        sum_qs = TankosAplsummary.objects.values(
            'gid',
            'afdeling',
            'block',
            'ha',
            'target_tonase',
            'target_pokok',
            'prog_tonase',
            'prog_pokok',
            'app_sph',
            'prog_ha',
            'last_date',
            ).filter(block__contains=query) # TODO: Paginate table to 15 item

        ## Checking available data
        if sum_qs is None:
            messages.warning("Data isn't available")
            return redirect('AplSummary')

        else:
            ## Context dictionary for passing data
            context = {
                'Title': Title,
                'TableData' : sum_qs,
            }

    else:
        ## Data collecting and cleansing from database
        sum_qs = TankosAplsummary.objects.values(
        'gid',
        'afdeling',
        'block',
        'ha',
        'target_tonase',
        'target_pokok',
        'prog_tonase',
        'prog_pokok',
        'app_sph',
        'prog_ha',
        'last_date',
        ) # TODO: Paginate table to 15 item

        ## Context dictionary for passing data
        context = {
            'Title': Title,
            'TableData' : sum_qs,
        }
    return render(request, "dashboard/static_tankosapl_table.html", context)

def AplPokokTable(request, geomid):
    Title = 'Dashboard - pokok'
    query = request.GET.get('q')
    if query:
        pokok_qs = TankosAplpokok.objects.filter(geomid=geomid).filter(date__contains=query).order_by('-date')

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
        pokok_qs = TankosAplpokok.objects.filter(geomid=geomid).order_by('-date') #TODO: Paginate table to 15 item

        ## Context dictionary for passing data
        context = {
            'Title': Title,
            'TableData' : pokok_qs,
        }
    return render(request, "dashboard/static_tankospokok_table.html", context)

def AplTonaseTable(request, geomid):
    Title = 'Dashboard - tonase'
    query = request.GET.get('q')
    if query:
        tonase_qs = TankosApltonase.objects.filter(geomid=geomid).filter(date__contains=query).order_by('-date')

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
        tonase_qs = TankosApltonase.objects.filter(geomid=geomid).order_by('-date') #TODO: Paginate table to 15 item

        ## Context dictionary for passing data
        context = {
            'Title': Title,
            'TableData' : tonase_qs,
        }
    return render(request, "dashboard/static_tankostonase_table.html", context)


## Dump
def DumpTable(request):
    Title = 'Dashboard - dump'
    query = request.GET.get('q')
    if query:
        dump_qs = TankosDumpdata.objects.filter(location__contains=query).order_by('dump_date')

        ## Checking available data
        if dump_qs is None:
            messages.warning("Data isn't available")
            time.sleep(5)
            return redirect('DumpTable')

        else:
            ## Context dictionary for passing data
            context = {
                'Title': Title,
                'TableData' : dump_qs,
            }

    ## Data collecting and cleansing from database
    dump_qs = TankosDumpdata.objects.all().order_by('dump_date') #TODO: Paginate table to 15 item

    ## Context dictionary for passing data
    context = {
        'Title': Title,
        'TableData' : dump_qs,
    }
    return render(request, "dashboard/static_tankosdump_table.html", context)

@login_required(login_url="")
def DumpEdit(request, gid):

    title = 'Edit Dump'
    dumps_obj = get_object_or_404(TankosDumpdata, gid=gid)
    geom_id = dumps_obj.location

    if request.method == 'POST':
        form = EditDumpForm(request.POST, instance=dumps_obj)
        if form.is_valid():
            dumps_obj = form.save(commit=False)
            dumps_obj.status = 'Bagus'
            dumps_obj.save()

            messages.success(request, 'Blok updated successfully.')
            return redirect('DumpTable')
        else:
            # Form is not valid, display form errors
            error_message = "Error updating blok. Please check your input."
            print("Error updating blok:", form.errors)
            messages.error(request, error_message)
    else:
        form = EditDumpForm(instance=dumps_obj)

    context = {
        'form': form,
        'title': title,
        'geomid': geom_id,
    }
    return render(request, "dashboard/static_tankosdump_table_edit.html", context)



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

    title = 'Edit Jangkos'
    # patok_obj = HguPatok.objects.values().filter(gid=gid)
    patok_obj = get_object_or_404(HguPatok, gid=gid)

    if request.method == 'POST':
        form = EditPatokForm(request.POST, instance=patok_obj)
        if form.is_valid():
            patok_obj = form.save(commit=False)
            patok_obj.status = 'Bagus'
            patok_obj.save()

            messages.success(request, 'Blok updated successfully.')
            return redirect('PatokTable')
        else:
            # Form is not valid, display form errors
            error_message = "Error updating blok. Please check your input."
            print("Error updating blok:", form.errors)
            messages.error(request, error_message)
    else:
        form = EditPatokForm(instance=patok_obj)

    context = {
        'form': form,
        'title': title,
        'geomid': gid,
    }
    return render(request, "dashboard/static_patok_table_edit.html", context)


## Pupuk
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