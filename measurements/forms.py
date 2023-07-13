from django import forms
from .models import Measurement, Device
from experiments.models import Experiment
from django.core.exceptions import ValidationError
import csv
class AddFileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk")
        super(AddFileForm,self).__init__(*args, **kwargs)
        self.fields["experiment"].queryset = Experiment.objects.all()
        self.fields["experiment"].initial = Experiment.objects.get(id=self.pk)

    device = forms.ModelChoiceField(queryset=Device.objects.all(), empty_label="---------")
    file = forms.FileField()
    is_approved = forms.BooleanField(initial=True)

    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('file')
        if csv_file:
            # Read the CSV file
            csv_data = csv.reader(csv_file)

            # Check the number of columns
            for row in csv_data:
                if len(row) != 3:
                    raise forms.ValidationError('The CSV file must have exactly three columns.')

        return csv_file


    class Meta:
        model = Measurement
        fields = ['experiment', 'device', 'file', 'is_approved']
