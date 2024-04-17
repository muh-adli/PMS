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
    # print(type(TableData))
    # print(TableData)

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
    JembatanCount_qs = Jembatan.objects.count()
    # print(JembatanCount_qs)
    JembatanKondisi_qs = Jembatan.objects.values('kondisi').annotate(count=Count('kondisi'))
    # print(JembatanKondisi_qs)
    JembatanBaik = JembatanRusak = JembatanBaru = JembatanNone= 0
    for jemb in JembatanKondisi_qs:
        if jemb['kondisi'] == 'BAIK':
            JembatanBaik = jemb['count']
        elif jemb['kondisi'] == 'RUSAK':
            JembatanRusak = jemb['count']
        elif jemb['kondisi'] == 'Baru':
            JembatanBaru = jemb['count']
    JembatanNone = JembatanCount_qs - (JembatanBaik + JembatanRusak + JembatanBaru)
    print(JembatanBaik,JembatanRusak,JembatanBaru,JembatanNone)
    JembatanTotal = JembatanBaik + JembatanRusak + JembatanBaru + JembatanNone
    print(JembatanTotal)
    JembatanPerc = round((JembatanBaik+JembatanBaru)/JembatanTotal*100, 2)
    # print(JembatanPerc)

    PatokKode_qs = MonitoringPatokhgu.objects.count()
    # print(PatokKode_qs)
    PatokPeriode_qs = MonitoringPatokhgu.objects.values('periode').annotate(count=Count('periode'))
    # print(PatokPeriode_qs)
    PatokQ1 = PatokQ2 = PatokQ3 = PatokQ4 = 0
    for patok in PatokPeriode_qs:
        if patok['periode'] == 'Q1':
            PatokQ1 = patok['count']
        elif patok['periode'] == 'Q2':
            PatokQ2 = patok['count']
        elif patok['periode'] == 'Q3':
            PatokQ3 = patok['count']
        elif patok['periode'] == 'Q4':
            PatokQ4 = patok['count']
    PatokNone = PatokKode_qs - (PatokQ1 + PatokQ2 + PatokQ3 + PatokQ4)
    print(PatokQ1, PatokQ2, PatokQ3, PatokQ4, PatokNone)
    PatokPrec = round((PatokQ1 + PatokQ2 + PatokQ3 + PatokQ4)/PatokKode_qs*100, 2)
    # print(PatokPrec)
    
    ## Visualization
    ## Color pallete
    color3 = ['#003f5c','#bc5090','#ffa600']
    color4 = ['#003f5c','#7a5195','#ef5675','#ffa600']
    color5 = ['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']
    color6 = ['#003f5c','#444e86','#955196','#dd5182','#ff6e54','#ffa600']
    color7 = ['#003f5c','#374c80','#7a5195','#bc5090','#ef5675','#ff764a','#ffa600']
    color8 = ['#003f5c','#2f4b7c','#665191','#a05195','#d45087','#f95d6a','#ff7c43','#ffa600']

    ## Data cleansing
    LabelJembatan = ['Baik', 'Rusak', 'Baru', 'N/A']
    ValueJembatan = [JembatanBaik, JembatanRusak, JembatanBaru, JembatanNone]

    LabelPatok = ['Q1','Q2','Q3','Q4','N/A',]
    ValuePatok = [PatokQ1, PatokQ2, PatokQ3, PatokQ4, PatokNone]

    ## Plotting
    fig = make_subplots(rows=1,cols=2,
                        specs=[
                                [{"type": "domain"}, {"type": "domain"}],
                            ],
                        subplot_titles=(
                            "Bridge Condition",
                            "Periods Patok HGU")
                        )

    fig.add_trace(
        go.Pie(name='',
            values = LabelJembatan,
            labels = ValueJembatan,
            hovertemplate = "Kondisi %{label}: %{value}"
        ),
        row=1, col=1)
    fig.update_traces(textinfo='value', textfont_size=20,
                    marker=dict(colors=color4, line=dict(color='#000000', width=1)))

    fig.add_trace(
        go.Pie(name='',
            values = LabelPatok,
            labels = ValuePatok,
            hovertemplate = "Kategori:  %{label}"
        ),
        row=1, col=2)
    fig.update_traces(textinfo='value', textfont_size=20,
                    marker=dict(colors=color5, line=dict(color='#000000', width=1)))
    # Render the plot as HTML code
    plot_fig = fig.to_html()

    # Context dictionary for passing data
    context = {
        'Title': Title,
        'JembatanPerc': JembatanPerc,  # Percentage Data of Bridge Conditions
        'PatokPrec': PatokPrec,  # Percentage Data of Patok Periods
        'plot_fig': plot_fig,
    }
    return render(request, "dashboard/asd.html", context)