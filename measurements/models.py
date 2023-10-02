from django.db import models
from requests import delete
from experiments.models import Experiment, Company
from django.utils.html import format_html
from django.apps import apps


class Device(models.Model):
    # id
    model = models.CharField(max_length=127)
    company = models.ForeignKey(
       Company , on_delete=models.CASCADE, related_name='company_id')

    def __str__(self):
        return f"{self.company}: {self.model}"

    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'


# class Machine(models.Model):
#     # id
#     model = models.CharField(max_length=127)
#     company = models.ForeignKey(
#        Company , on_delete=models.CASCADE, related_name='companyid')

#     def __str__(self):
#         return f"{self.company}: {self.model}"

#     class Meta:
#         verbose_name = 'Machine'
#         verbose_name_plural = 'Machines'

class Measurement(models.Model):

    # id
    experiment = models.ForeignKey(
       Experiment , on_delete=models.CASCADE, related_name="getMeasurement")
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    file = models.FileField(upload_to='measurements/')
    is_approved = models.BooleanField(
        default=True)  # set to False in production
    # type (NMR, Mn, ...) -> is this a Device or Measurement attribute?

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = 'Measurement'
        verbose_name_plural = 'Measurements'


class Data(models.Model):
    # id

    # if a measurement gets deleted, delete the data as well.
    measurement = models.ForeignKey(
        Measurement, on_delete=models.CASCADE, related_name="measurement")
    res_time = models.FloatField()
    result = models.FloatField()
    d = models.CharField(max_length=100, null=True)
    mn = models.CharField(max_length=100, null=True)
    # is_outlier     a function can identify outliers and set this flag so this data can be hidden if needed


