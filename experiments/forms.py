from django import forms
from experiments.models import *
from users.models import User, User_Group, Group
from .models import Company
from chemicals.models import InChi
from measurements.models import Data, Measurement

class AddReactorForm(forms.ModelForm):
    #we need to pass the request to get the user so we can get all the groups that the user is part of
    #we search the User_Group table for a list of group ids via .values_list('group') and use that list as a filter for Group ids
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddReactorForm,self).__init__(*args, **kwargs)
        self.fields["group"].queryset = Group.objects.filter(id__in=User_Group.objects.filter(user=self.request.user).values_list('group_id'))

    TYPE_CHOICES = (
        ('-', '---------'),
        ('B', 'Batch'),
        ('F', 'Flow'),
    )

    name = forms.CharField()
    volume = forms.FloatField()
    type = forms.ChoiceField(choices = TYPE_CHOICES)
    

    class Meta:
        model = Reactor
        fields = ['name', 'volume', 'type', 'group']



class AddChemicalForm(forms.ModelForm):
    #we need to pass the request to get the user so we can get all the groups that the user is part of
    #we search the User_Group table for a list of group ids via .values_list('group') and use that list as a filter for Group ids
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddChemicalForm,self).__init__(*args, **kwargs)
        self.fields["group"].queryset = Group.objects.filter(id__in=User_Group.objects.filter(user=self.request.user).values_list('group'))

    inchi = forms.ModelChoiceField(queryset=InChi.objects.all(), empty_label="---------")
    company = forms.ModelChoiceField(queryset=Company.objects.order_by('name'), empty_label="---------")
    purity = forms.FloatField(required=False)
    extra_info = forms.CharField(required=False, max_length=511, widget=forms.Textarea(attrs={"rows":5}))
    url = forms.URLField(required=False, max_length=511)

    class Meta:
        model = Inventory
        fields = ['inchi', 'company', 'purity', 'extra_info', 'url', 'group']

class AddExperimentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddExperimentForm, self).__init__(*args, **kwargs)
        experiment_last = Experiment.objects.filter(
        user_id__in=User_Group.objects.filter(
        group_id__in=User_Group.objects.filter(
        user_id=self.request.user.id)
        .values_list('group_id', flat=True))
        .values_list('user_id', flat=True)).last()

        if experiment_last:

            self.fields['name'].widget.attrs['value'] = experiment_last.name
            self.fields['time'].widget.attrs['value'] = experiment_last.time
            self.fields['date'].widget.attrs['value'] = experiment_last.date
            self.fields['temperature'].widget.attrs['value'] = experiment_last.temperature
            self.fields['total_volume'].widget.attrs['value'] = experiment_last.total_volume
            self.fields['reactor'].widget.attrs['value'] = experiment_last.reactor
        
    
    date = forms.DateField()
    time = forms.TimeField()
    name = forms.CharField(max_length=127)
    temperature = forms.FloatField()
    total_volume = forms.FloatField()
    reactor =  forms.MultipleChoiceField(choices=[(r.pk, r.__str__()) for r in Reactor.objects.all()], required=False)
    equipment= forms.MultipleChoiceField(choices=[(e.pk, e.__str__()) for e in Equipment.objects.all()], required=False)


    class Meta:
        model = Experiment
        fields = ['date', 'time', 'name', 'temperature', 'total_volume', 'reactor', 'equipment']

class UpdateExperimentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk")
    
    class Meta:
        model = Experiment
        fields = ['name', 'temperature', 'total_volume', 'reactor']


class AddIngredientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk")
        super(AddIngredientForm,self).__init__(*args, **kwargs)
        self.fields["experiment"].queryset = Experiment.objects.all()
        self.fields["experiment"].initial = Experiment.objects.get(id=self.pk)

    TYPE_CHOICES = (
        ('-', '---------'),
        ('M', 'Monomer'),
        ('I', 'Initiator'),
        ('S', 'Solvent'),
        ('O', 'Other'),
    )

    inventory = forms.ModelChoiceField(queryset=Inventory.objects.all(), empty_label="---------")
    type = forms.ChoiceField(choices=TYPE_CHOICES)
    molarity = forms.FloatField()

    class Meta:
        model = Experiment_Chemicals
        fields = ['experiment', 'inventory', 'type', 'molarity']



class AddEquipmentForm(forms.ModelForm):
    #we need to pass the request to get the user so we can get all the groups that the user is part of
    #we search the User_Group table for a list of group ids via .values_list('group') and use that list as a filter for Group ids
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddEquipmentForm,self).__init__(*args, **kwargs)
        self.fields["group"].queryset = Group.objects.filter(id__in=User_Group.objects.filter(user=self.request.user).values_list('group'))
    serial_number = forms.CharField(max_length=256)
    vendor = forms.ModelChoiceField(queryset=Company.objects.all(), empty_label="---------", required=False)
    details = forms.CharField(required=False, max_length=511, widget=forms.Textarea(attrs={"rows":5}))

    class Meta:
        model = Equipment
        fields = ['serial_number', 'vendor', 'details', 'group']

from measurements.models import Device
class AddFilenameForm(forms.ModelForm):
    file = forms.CharField(required=True, max_length=128)
    device =forms.ModelChoiceField(queryset=Device.objects.all(), empty_label="---------", required=False)
    class Meta:
        model = Measurement
        fields = ['file', 'device']


class AddDataForm(forms.ModelForm):
    #we need to pass the request to get the user so we can get all the groups that the user is part of
    #we search the User_Group table for a list of group ids via .values_list('group') and use that list as a filter for Group ids
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddDataForm,self).__init__(*args, **kwargs)
        # self.fields["measurement_id"].queryset = Data.objects.filter(measurement=Measurement.objects.get(experiment = pk)).values_list('measurement_id', flat=True)[0]   
    res_time = forms.FloatField()
    result = forms.FloatField()
    mn = forms.FloatField()
    d = forms.FloatField()

    class Meta:
        model = Data
        fields = ['res_time', 'result', 'mn', 'd']



class AddExperimentReagentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk")
        super(AddExperimentReagentForm,self).__init__(*args, **kwargs)
        self.fields["experiment"].queryset = Experiment.objects.all()
        self.fields["experiment"].initial = Experiment.objects.get(id=self.pk)

    reagent_info = forms.ModelChoiceField(queryset=Reagent_Info.objects.all().order_by('name'), empty_label="---------")
    concentration = forms.FloatField()

    class Meta:
        model = Experiment_Reagent
        fields = ['experiment', 'reagent_info', 'concentration']


from chemicals.models import Name
class AddReagentInfoForm(forms.ModelForm):
    #we need to pass the request to get the user so we can get all the groups that the user is part of
    #we search the User_Group table for a list of group ids via .values_list('group') and use that list as a filter for Group ids
    last_chemical_name = Name.objects.filter(iupac=True).last()
    name = forms.CharField(max_length=128)
    chemical_name = forms.ModelChoiceField(queryset=Name.objects.filter(iupac=True).order_by('-id'), initial=Name.objects.filter(iupac=True).order_by('-id').first(), required=True)
    reagent = forms.ModelChoiceField(queryset=Reagent.objects.all(), empty_label="---------", required=True)

    class Meta:
        model = Reagent_Info
        fields = ['name', 'reagent', 'chemical_name']

