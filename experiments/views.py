from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from chemicals.views import add_reagent_info
from experiments.forms import *
from measurements.models import Measurement, Device, Data
from .models import Experiment, Experiment_Chemicals, Reactor, Inventory, Equipment
from .tables import EquipmentTable, ExperimentTable, SupplierTable, SuppliesTable, ReactorTable, ExperimentReagentTable
from measurements.forms import AddFileForm
from measurements.tables import MeasurementTable
from users.models import User_Group
# from django.contrib.auth.models import User
from django.http import Http404
from .decorators import group_required


@login_required
@group_required

def my_experiments(request):
    experiments = Experiment.objects.all()
    is_leader=False
    try:
        current_user = request.user.id
        group = list(User_Group.objects.filter(user = current_user).values_list('group_id', flat=True))[0]
        users_in_group = list(User_Group.objects.filter(group_id = group).values_list('user_id', flat=True))
        experiments_list=[]
        for exp in experiments:
            if exp.user_id in users_in_group:
                experiments_list.append(exp) 
        experiments= experiments_list
        user_id = request.user.id
        is_leader = User_Group.objects.filter(user_id=user_id).values_list('is_leader', flat=True)[0]
        print('isleader', is_leader)
    except:
        pass
    
    
    context = {
        'experiments': experiments,
        'is_leader': is_leader
    }

    return render(request, "experiments/my_experiments.html", context)


@login_required
@group_required
def my_chemicals(request):

    chemicals = SupplierTable(Inventory.objects.all())

    context = {
        'chemicals': chemicals,
    }

    return render(request, "experiments/my_chemicals.html", context)


@login_required
@group_required

def my_reactors(request):
    gp_id = User_Group.objects.filter(user_id=request.user.id).values_list('group_id', flat=True)[0]
    reactors = ReactorTable(Reactor.objects.filter(group_id=gp_id))

    context = {
        'equipment': reactors,
    }

    return render(request, "experiments/my_reactors.html", context)


@login_required
@group_required

def add_reactor(request):
    if request.method == 'POST':
        form = AddReactorForm(request.POST, request=request)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your equipment was successfully added')
            return redirect(to='my_reactors')

    else:
        form = AddReactorForm(request=request)

    context = {
        'form': form
    }

    return render(request, "experiments/add_reactor.html", context)


@login_required
@group_required

def add_supplier(request):
    if request.method == 'POST':
        form = AddChemicalForm(request.POST, request=request)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your chemical was successfully added')
            return redirect(to='my_chemicals')

    else:
        form = AddChemicalForm(request=request)

    context = {
        'form': form
    }

    return render(request, "experiments/add_chemical.html", context)


@login_required
@group_required

def add_experiment(request):
    last_exp=None
    if request.method == 'POST':
        form = AddExperimentForm(request.POST,  request=request)
        print(form.instance.name)

        if form.is_valid():
            form.instance.user= request.user
            form.save()
            messages.success(request, 'Your experiment was successfully added')
            last_exp_user = Experiment.objects.filter(user=request.user.id).last()
            return redirect(to=experiment_detail, pk=last_exp_user.id, error=0)
        else:
            print(form.errors)
        last_exp=Experiment.objects.order_by('-id').first()
        print(last_exp)

    else:
        print(request.user.email)
        form = AddExperimentForm( request=request)

    experiment_last = Experiment.objects.filter(
        user_id__in=User_Group.objects.filter(
        group_id__in=User_Group.objects.filter(
        user_id=request.user.id)
        .values_list('group_id', flat=True))
        .values_list('user_id', flat=True)).last()
    

    

    context = {
        'form': form,
        'user_id' : request.user.first_name + " " + request.user.last_name,
        'last_exp': last_exp,
        'experiment_last': experiment_last
    }

    return render(request, "experiments/add_experiment.html", context)


import pandas as pd
from datetime import timedelta
def csv_to_db(file, pk):

    data = pd.read_csv(file.file, encoding='UTF-8')
    data.dropna(subset=['conversion', 'tres'], inplace=True)
    data_conv = data[['conversion', 'tres']]
    data_conv['tres'] = data_conv.apply(
        lambda row: timedelta(minutes=row.tres).total_seconds(), axis=1)
    data_conv.rename(columns={'conversion': 'Conversion %',
                     'tres': 'res_time'}, inplace=True)
    data_conv['measurement_id'] = pk

import csv
from .forms import UpdateExperimentForm

@login_required
@group_required

def experiment_detail(request, pk, error):

    experiment = Experiment.objects.get(pk=pk)
    signed_in_user = request.user.id
    experiment_user = experiment.user.id
    experiment_user_group = User_Group.objects.filter(user=experiment_user).values_list("group", flat=True)
    signed_in_user_group = User_Group.objects.filter(user=signed_in_user).values_list("group", flat=True)

    if signed_in_user_group[0] != experiment_user_group[0]:
        raise Http404("This page does not exist")

    if request.method == 'POST':
        form = AddExperimentReagentForm(request.POST, pk=pk)
        if form.is_valid():
            form.save()
            return redirect('experiment_detail', pk=pk, error=0)
        else:
            print('column error')
    else:
        form = AddExperimentReagentForm(pk=pk)





    if request.method == 'POST' and request.FILES:
        csv_file = request.FILES['file']
        csv_data = csv.reader(csv_file)
        form = AddFileForm(request.POST, pk=pk)

        if form.is_valid():
            # csv_file = form.cleaned_data['csv_file']
            # file_content = csv_file.read()
            form.save()
            return redirect('experiment_detail', pk=pk, error=0)
        else:
            print('column error')
    else:
        # csv_file = request.FILES['file']
        # print(csv_file)
        # form = AddFileForm(pk=pk)
        experiment = Experiment.objects.get(id=pk)
        supplies = SuppliesTable(
            Experiment.objects.filter(id=pk))
        file_form = AddFileForm(pk=pk)
        files_list = MeasurementTable(Measurement.objects.filter(experiment=pk))
        # files_list = Measurement.objects.all()
    
    data_table=[]
    if request.method == 'POST':

        form_filename = AddFilenameForm(request.POST)

        if form_filename.is_valid():
            form_filename.instance.experiment_id = pk
            form_filename.save()
            filename_id = form_filename.instance.id
            messages.success(request, 'Your Data was successfully added')
            return redirect(to='add_csv_data', pk=filename_id)
        else:
            print(form_filename.errors)
    else:

        form_filename = AddFilenameForm()
        
    
    
    ratios=[]
    reagents=[]
    reagents_ratio=[]

    concentrations = list(Experiment_Reagent.objects.filter(experiment=pk).values_list('concentration', flat=True))     
    if concentrations:
        min_concentration = min(concentrations)
        ratios = [round(int(i)/int(min_concentration), 2) for i in concentrations]
        reagents = Experiment_Reagent.objects.filter(experiment=pk)
        # for i in range(len(ratios)):
        #     reagents[i]['ratios'] = ratios[i]
        reagents_ratio = []
        for i in range(len(reagents)):
            reagents_ratio.append({'id': str(reagents[i].id),'reagent_info': str(reagents[i].reagent_info),
                                'concentration': str(reagents[i].concentration),
                                'ratio': str(ratios[i])})


        print(reagents_ratio)
    


    context = {
        'experiment': experiment,
        'files_list': files_list,
        'file_form': file_form,
        'supplies': supplies,
        'form': form,
        'pk': pk,
        'form_filename':form_filename,
        'error': error,
        'experimentReagentTable': reagents,
        'ratios' : ratios,
        'reagents_ratio': reagents_ratio,
        'data_table':data_table
    
    }

    return render(request, "experiments/experiment.html", context)


@login_required
@group_required

def experiment_detail_delete(request, pk):
    if request.method == 'POST':
        return redirect('experiment_detail', pk=pk)
    


@login_required
@group_required

def equipments(request):
    gp_id = User_Group.objects.filter(user_id=request.user.id).values_list('group_id', flat=True)[0]

    equipments = EquipmentTable(Equipment.objects.filter(group_id=gp_id))

    context = {
        'equipments': equipments,
    }

    return render(request, "experiments/equipments.html", context)
@login_required
@group_required

def insert_equipment(request):
    if request.method == 'POST':
        form = AddEquipmentForm(request.POST, request=request)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your experiment was successfully added')
            return redirect(to='equipments')
        else:
            print(form.errors)

    else:
        # print(request.user.email)
        form = AddEquipmentForm(request=request)

    context = {
        'form': form,
    }

    return render(request, "experiments/insert_equipment.html", context)



import json

from django.http import HttpResponse
@group_required

def experiment_test(request):
    names = list(Experiment.objects.values_list('name', flat=True))
    result = {"names": names}
    return HttpResponse(json.dumps(result), content_type="application/json")


from django.shortcuts import get_object_or_404, redirect

@group_required

def delete_reagent(request, object_id):
    # Step 2: Retrieve the object
    obj = get_object_or_404(Experiment_Reagent, pk=object_id)
    obj.delete()
    return redirect(experiment_detail, pk=obj.experiment.id, error=0)  # Redirect to some success page

@group_required

def delete_experiment(request, object_id):
    # Step 2: Retrieve the object
    obj = get_object_or_404(Experiment, pk=object_id)
    obj.delete()
    return redirect(my_experiments)  # Redirect to some success page

@group_required

def edit_experiment(request, item_id):
    item = get_object_or_404(Experiment, pk=item_id)
    
    if request.method == 'POST':
        form = AddExperimentForm(request.POST, request=request, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_detail', item_id=item_id)
    else:
        form = AddExperimentForm(request=request, instance=item)
    
    return render(request, 'add_experiment.html', {'form': form, 'item': item})



@group_required
def delete_data(request, item, fk):
    print("delete pk", item)
    obj = get_object_or_404(Data, pk=item)
    obj.delete()
    return redirect(add_csv_data, pk=fk)  # Redirect to some success page

def add_csv_data(request, pk):
    print(pk)
    data_table = list(Data.objects.filter(measurement_id=pk))
    if request.method == 'POST':
        form = AddDataForm(request.POST, request=request)
        form.instance.measurement_id = pk
        if form.is_valid():
            form.save()
            return redirect('add_csv_data', pk=pk)
    else:

        form = AddDataForm(request=request)
    return render(request, 'measurements/add_csv_data.html', {'data_table':data_table, 'form':form, 'pk':pk})


def edit_data(request, pk, fk):
    obj = get_object_or_404(Data, pk=pk)
    if request.method == 'POST':
        form = AddDataForm(request.POST, instance=obj, request=request)
        if form.is_valid():
            form.save()
            return redirect('add_csv_data', pk=fk)
    else:
        form = AddDataForm(instance=obj, request=request)

    return render(request, 'measurements/edit_csv_data.html', {'form': form, 'pk':pk, 'fk':fk})


