from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from experiments.forms import AddEquipmentForm, AddChemicalForm, AddExperimentForm, AddIngredientForm, AddReactorForm
from measurements.models import Measurement
from .models import Experiment, Experiment_Chemicals, Reactor, Inventory, Equipment
from .tables import EquipmentTable, ExperimentTable, SupplierTable, SuppliesTable, ReactorTable
from measurements.forms import AddFileForm
from measurements.tables import MeasurementTable
# from django.contrib.auth.models import User

@login_required
def my_experiments(request):

    experiments = ExperimentTable(Experiment.objects.all())

    context = {
        'experiments': experiments,
    }

    return render(request, "experiments/my_experiments.html", context)


@login_required
def my_chemicals(request):

    chemicals = SupplierTable(Inventory.objects.all())

    context = {
        'chemicals': chemicals,
    }

    return render(request, "experiments/my_chemicals.html", context)


@login_required
def my_reactors(request):

    equipment = ReactorTable(Reactor.objects.all())

    context = {
        'equipment': equipment,
    }

    return render(request, "experiments/my_reactors.html", context)


@login_required
def add_reactor(request):
    if request.method == 'POST':
        form = AddReactorForm(request.POST, request=request)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your equipment was successfully added')
            return redirect(to='add_reactor')

    else:
        form = AddReactorForm(request=request)

    context = {
        'form': form
    }

    return render(request, "experiments/add_reactor.html", context)


@login_required
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
def add_experiment(request):
    if request.method == 'POST':
        form = AddExperimentForm(request.POST)

        if form.is_valid():
            form.instance.user= request.user
            form.save()
            messages.success(request, 'Your experiment was successfully added')
            return redirect(to='my_experiments')
        else:
            print(form.errors)

    else:
        print(request.user.email)
        form = AddExperimentForm()

    context = {
        'form': form,
        'user_id' : request.user.first_name + " " + request.user.last_name
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
@login_required
def experiment_detail(request, pk, error):
    if request.method == 'POST':
        form = AddIngredientForm(request.POST, pk=pk)
        if form.is_valid():
            form.save()
            return redirect('experiment_detail', pk=pk, error=0)
        else:
            print('column error')
    else:
        form = AddIngredientForm(pk=pk)

    # make sure this is not iterable: set correct permissions!

    

    # if request.method == 'POST':
    #     csv_file=request.FILES['file']
    #     df = pd.read_csv(csv_file)
    #     if "Scannumber" not in df.columns:
    #         return redirect("home")

    #     form = AddFileForm(request.POST, request.FILES, pk=pk)
    #     if form.is_valid():
    #         m = form.save()
    #         csv_to_db(m.file, m.pk)
    #     else:
    #         pass
            # print(form.errors)

    # return redirect('experiment_detail', pk=pk)



    if request.method == 'POST':
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
            Experiment_Chemicals.objects.filter(experiment=pk))
        file_form = AddFileForm(pk=pk)
        files_list = MeasurementTable(Measurement.objects.filter(experiment=pk))

    context = {
        'experiment': experiment,
        'files_list': files_list,
        'file_form': file_form,
        'supplies': supplies,
        'form': form,
        'pk': pk,
        'error': error
    }

    return render(request, "experiments/experiment.html", context)


@login_required
def experiment_detail_delete(request, pk):
    if request.method == 'POST':
        return redirect('experiment_detail', pk=pk)
    


@login_required
def equipments(request):
    equipments = EquipmentTable(Equipment.objects.all())

    context = {
        'equipments': equipments,
    }

    return render(request, "experiments/equipments.html", context)
@login_required
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

