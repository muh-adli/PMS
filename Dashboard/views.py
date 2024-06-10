## Django build-in fuctions
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count, Sum, Q, Min, Max


# Models and forms
from .models import *
from .forms import *
from .tables import *
from Map.models import *


## Library
from datetime import timedelta
import pandas as pd
from datetime import datetime
import io
import time
from datetime import datetime


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

    pokok_data = TankosAplpokok.objects.all()
    print(pokok_data)
    print(len(pokok_data))
    tonase_data = TankosApltonase.objects.all()
    dump_data = TankosDumpdata.objects.all()


    if len(pokok_data) == 0 and len(tonase_data) == 0 and len(dump_data) == 0 :
        print('masuk if')
        pokok_counts = []
        tonase_counts = []
        dump_counts = []

        ## Context
        context = {
            'Title':Title,
        }

    else:
        print('masuk else')
        # Aggregate min and max dates for each dataset
        pokok_min_date = pokok_data.aggregate(min_date=Min('date'))['min_date']
        pokok_max_date = pokok_data.aggregate(max_date=Max('date'))['max_date']

        tonase_min_date = tonase_data.aggregate(min_date=Min('date'))['min_date']
        tonase_max_date = tonase_data.aggregate(max_date=Max('date'))['max_date']

        dump_min_date = dump_data.aggregate(min_date=Min('dump_date'))['min_date']
        dump_max_date = dump_data.aggregate(max_date=Max('dump_date'))['max_date']

        # Initialize min_date and max_date to None
        min_date = None
        max_date = None

        # Collect all available min and max dates in a list
        all_min_dates = [pokok_min_date, tonase_min_date, dump_min_date]
        all_max_dates = [pokok_max_date, tonase_max_date, dump_max_date]

        # Filter out None values
        valid_min_dates = [date for date in all_min_dates if date is not None]
        valid_max_dates = [date for date in all_max_dates if date is not None]

        # Compute min_date and max_date if there are any valid dates
        if valid_min_dates:
            min_date = min(valid_min_dates)
        if valid_max_dates:
            max_date = max(valid_max_dates)

        # Generate all dates between min and max date if both dates are valid
        all_dates = []
        all_date_str = []
        if min_date and max_date:
            all_dates = [min_date + timedelta(days=x) for x in range((max_date - min_date).days + 1)]
            all_date_str = [(min_date + timedelta(days=x)).strftime("%Y-%m-%d") for x in range((max_date - min_date).days + 1)]

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
        ## Context
        context = {
            'Title':Title,
            'all_dates': all_date_str,
            'pokok_counts':pokok_counts,
            'tonase_counts':tonase_counts,
            'dump_counts':dump_counts,
            'min_date': min_date,
            'max_date': max_date,
        }
    # print('Pokok: ', pokok_counts)
    # print('Tonase: ', tonase_counts)
    # print('Dump: ', dump_counts)



    # ## Context
    # context = {
    #     'Title':Title,
    #     'all_dates': all_date,
    #     'pokok_counts':pokok_counts,
    #     'tonase_counts':tonase_counts,
    #     'dump_counts':dump_counts,
    #     'min_date': min_date,
    #     'max_date': max_date,
    # }
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
            'tot_tonase',
            'tot_pokok',
            'prog_tonase',
            'prog_pokok',
            'sph',
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
            'tot_tonase',
            'tot_pokok',
            'prog_tonase',
            'prog_pokok',
            'sph',
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

    modalData = TankosAplgeom.objects.values(
        'afdeling',
        'block',
        'gid',
    )
    choices = {}

    for item in modalData:
        afdeling = item['afdeling']
        block = item['block']
        gid = item['gid']
        if afdeling in choices:
            choices[afdeling].append({'block': block, 'gid': gid})
        else:
            choices[afdeling] = [{'block': block, 'gid': gid}]

    for afdeling, blocks in choices.items():
        choices[afdeling] = sorted(blocks, key=lambda x: x['block'])
    # print(choices)

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
                'choices': choices,
                'geomid': geomid,
            }

    else:
        ## Data collecting and cleansing from database
        pokok_qs = TankosAplpokok.objects.filter(geomid=geomid).order_by('-date') #TODO: Paginate table to 15 item

        ## Context dictionary for passing data
        context = {
            'Title': Title,
            'TableData' : pokok_qs,
            'choices': choices,
            'geomid': geomid,
        }
    return render(request, "dashboard/static_tankospokok_table.html", context)


def AplPokokEdit(request):
    check_qs = TankosAplgeom.objects.values(
        'afdeling',
        'block',
        'gid',
    ).order_by('gid')
    # print(check_qs)

    # print(request.POST)
    if request.method == "POST":
        print("masuk POST")

        # Convert POST values to string to match with database values
        afdeling = str(request.POST['afdeling'])
        block = str(request.POST['block'])
        geomid = request.POST['geomid']
        date = request.POST.get('date')
        pokok = request.POST.get('pokok')
        
        # print(afdeling)
        # print(block)
        # print(geomid)
        # print(date)
        # print(pokok)

        # Check if any object in the queryset matches the POST parameters
        exists = False
        for obj in check_qs:
            if obj['afdeling'] == afdeling and obj['block'] == block and str(obj['gid']) == geomid:
                exists = True

        if exists:
            print("Data masuk")
            if date and pokok:
                if TankosAplpokok.objects.filter(afdeling=afdeling, block=block, date=date).exists():
                    # formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%y')
                    messages.warning(request, f"Data on {afdeling}, {block} on {date} already exists.")
                else:
                    data ={
                        'afdeling': afdeling,
                        'block': block,
                        'date': date,
                        'pokok': pokok,
                        'geomid': geomid,
                    }
                    print(data)
                    form = addPokokForm(data=data)
                    if form.is_valid():
                        print("Form Valid")
                        form.save()
                        messages.success(request, "Data added successfully.")
                    else:
                        print("form invalid")
            else:
                print("date and pokok invalid")
                messages.warning(request,  "Invalid Data")
            ## TODO: validate form and input into database
        else:
            print("Data invalid")
            messages.warning(request,  "Invalid Data")
    else:
        print("gamasuk POST")
        messages.error(request, "Error in input data")
        
    return redirect('AplPokokTable', geomid=geomid)
        ## TODO: add new data based on afdeling and block

def AplTonaseTable(request, geomid):
    Title = 'Dashboard - tonase'
    query = request.GET.get('q')

    modalData = TankosAplgeom.objects.values(
        'afdeling',
        'block',
        'gid',
    )
    choices = {}

    for item in modalData:
        afdeling = item['afdeling']
        block = item['block']
        gid = item['gid']
        if afdeling in choices:
            choices[afdeling].append({'block': block, 'gid': gid})
        else:
            choices[afdeling] = [{'block': block, 'gid': gid}]

    for afdeling, blocks in choices.items():
        choices[afdeling] = sorted(blocks, key=lambda x: x['block'])
    # print(choices)

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
                'choices': choices,
                'geomid': geomid,
            }
    else:
        ## Data collecting and cleansing from database
        tonase_qs = TankosApltonase.objects.filter(geomid=geomid).order_by('-date') #TODO: Paginate table to 15 item

        ## Context dictionary for passing data
        context = {
            'Title': Title,
            'TableData' : tonase_qs,
            'choices': choices,
            'geomid': geomid,
        }
    return render(request, "dashboard/static_tankostonase_table.html", context)

def AplTonaseEdit(request):
    check_qs = TankosAplgeom.objects.values(
        'afdeling',
        'block',
        'gid',
    ).order_by('gid')
    # print(check_qs)

    # print(request.POST)
    if request.method == "POST":
        print("masuk POST")
        # print(request.POST.get('afdeling'))
        # print(request.POST.get('block'))
        # print(request.POST.get('geomid'))

        # Convert POST values to string to match with database values
        afdeling = str(request.POST['afdeling'])
        block = str(request.POST['block'])
        geomid = request.POST['geomid']
        date = request.POST.get('date')
        tonase = request.POST.get('tonase')
    # Check if any object in the queryset matches the POST parameters
        exists = False
        for obj in check_qs:
            if obj['afdeling'] == afdeling and obj['block'] == block and str(obj['gid']) == geomid:
                exists = True

        if exists:
            print("Data masuk")
            if date and tonase:
                if TankosApltonase.objects.filter(afdeling=afdeling, block=block, date=date).exists():
                    formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%y')
                    messages.warning(request, f"Data on {afdeling}, {block} on {formatted_date} already exists.")
                else:
                    data ={
                        'afdeling': afdeling,
                        'block': block,
                        'date': date,
                        'tonase': tonase,
                        'geomid': geomid,
                    }

                    form = addTonaseForm(data=data)
                    if form.is_valid():
                        print("Form Valid")
                        form.save()
                        messages.success(request, "Data added successfully.")
            else:
                print("Data invalid")
                messages.warning(request,  "Invalid Data")
            ## TODO: validate form and input into database
        else:
            print("Data invalid")
            messages.warning(request,  "Invalid Data")
    else:
        print("gamasuk POST")
        messages.error(request, "Error in input data")
        
    return redirect('AplTonaseTable', geomid=geomid)
        ## TODO: add new data based on afdeling and block


## Dump
def DumpTable(request):
    Title = 'Dashboard - dump'
    query = request.GET.get('q')
    print(query)
    if query:
        print("masuk query")
        dump_qs = TankosDumpview.objects.filter(
            location__icontains=query
            ).order_by(
                'location'
            )

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
        dump_qs = TankosDumpview.objects.all(
                ).order_by(
                    'location'
                ) #TODO: Paginate table to 15 item

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
    print('Total periode: ', periode_counts)

    for key, value in periode_counts.items():
        list_key.append(key)
        list_value.append(value)

    # print(list_key)
    # print(list_value)

    ## Table
    patokTable = HguPatok.objects.exclude(update_date__isnull=True).order_by('-update_date')[:5]
    # print(patokTable)
    # table = PatokDashboardTable(patokTable)

    ## Context dictionary for passing data
    context = {
        'Title' : Title,
        'periode' : list_key,
        'count' : list_value,
        'patokTable' : patokTable,
        # 'table' : table,
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
        patok_qs = HguPatok.objects.all().order_by('no_patok')
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
        # Create a mutable copy of the POST data
        post_data = request.POST.copy()
        
        # Retrieve the periode value from the POST data
        periode = post_data.get('periode', '')

        # Set periode to None if it is an empty string
        if periode == '':
            print('masuk if')
            post_data['periode'] = ''
            patok_obj.periode = ''
            post_data['status'] = ''
            patok_obj.status = ''
            post_data['update_date'] = ''
            patok_obj.update_date = ''
        else:
            post_data['periode'] = periode
            patok_obj.periode = periode
            post_data['status'] = 'Baik'
            patok_obj.status = 'Baik'
            post_data['update_date'] = datetime.now()
            patok_obj.update_date = datetime.now()
        print(post_data)
        for k in post_data:
            print(k)

        # Create the form with the modified data
        form = EditPatokForm(post_data, instance=patok_obj)

        
        if form.is_valid():
            form.save()
            messages.success(request, 'Blok updated successfully.')
            return redirect('PatokTable')
        else:
            error_message = "Error updating patok data. Please check your input."
            print("Error on:", form.errors)
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