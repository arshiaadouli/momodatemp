from datetime import date
from django.db import models
from users.models import User, Group
from chemicals.models import InChi
from django.utils.html import format_html
# from measurements.models import cta, Monomer

class Initiator(models.Model):

    # id             = int, primary key, automatically provided
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Initiator'
        verbose_name_plural = 'Initiators'


class Monomer(models.Model):
    name = models.CharField(verbose_name="Monomer", max_length=511)
    # if a setup has an experiment the setup can't be deleted
    Mw = models.CharField(max_length=511)
    density_g_per_ml = models.CharField(max_length=511)
    boiling_point_celsius = models.CharField(max_length=511)
    vapour_pressure_kPa = models.CharField(max_length=511)
    viscosity_cP = models.CharField(max_length=511)
    c_number = models.CharField(max_length=511)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Monomer'
        verbose_name_plural = 'Monomers'


class cta(models.Model):
    name = models.CharField(verbose_name="Monomer", max_length=511)
    # if a setup has an experiment the setup can't be deleted
    Mw_cta = models.CharField(max_length=511)
    density_g_per_ml_cta = models.CharField(max_length=511)
    reflective_index_cta = models.CharField(max_length=511)
    boiling_point_c_cta = models.CharField(max_length=511)
    c_number_cta = models.CharField(max_length=511)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'cta'
        verbose_name_plural = 'cta'


class Reactor(models.Model):

    class Type(models.TextChoices):
        BATCH = 'B', 'Batch'
        FLOW = 'F', 'Flow'

    # id             = int, primary key, automatically provided
    name = models.CharField(max_length=30)
    volume = models.FloatField(verbose_name="Volume (ml)")
    type = models.CharField(max_length=1, choices=Type.choices)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Reactor'
        verbose_name_plural = 'Reactors'




class Company(models.Model):
    # id             = int, primary key, automatically provided
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Experiment(models.Model):
    # id             = int, primary key, automatically provided
    # if a user has an experiment the user can't be deleted
    # id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateField(default=date.today)
    time = models.TimeField()
    monomer = models.ForeignKey(Monomer, on_delete=models.CASCADE, default=None, blank=True, null=True)
    cta = models.ForeignKey(cta, on_delete=models.CASCADE, default=None, blank=True, null=True)
    initiator = models.ForeignKey(Initiator, on_delete=models.CASCADE, default=None, blank=True, null=True, related_name='initiator')
    
    monomer_concentration = models.FloatField(verbose_name="Monomer Concentration", null=True)
    
    cta_concentration = models.FloatField(verbose_name="CTA concentration", null=True)
    
    initiator_concentration = models.FloatField(verbose_name="Initiator Concentration", null=True)
    
    name = models.CharField(max_length=127)
    temperature = models.FloatField(verbose_name="Temperature (ºC)")
    total_volume = models.FloatField(verbose_name="Volume (ml)")
    reactor = models.ForeignKey(Reactor, on_delete=models.CASCADE, default=None, blank=True, null=True, related_name='reactor')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Experiment'
        verbose_name_plural = 'Experiments'


class Inventory(models.Model):
    # id             = int, primary key, automatically provided
    # can't delete a chemical that was used as a supply
    inchi = models.ForeignKey(
        InChi, on_delete=models.PROTECT, related_name="getInventory", verbose_name="Name")
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    purity = models.FloatField(null=True)
    extra_info = models.CharField(max_length=511, blank=True)
    url = models.URLField(max_length=511, blank=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.company}: {self.inchi}"

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventory'


class Experiment_Chemicals(models.Model):

    class Type(models.TextChoices):
        MONOMER = 'M', 'Monomer'
        INITIATOR = 'I', 'Initiator'
        SOLVENT = 'S', 'Solvent'
        OTHER = 'O', 'Other'

    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="getExperiments")
    type = models.CharField(max_length=1, choices=Type.choices)
    molarity = models.FloatField(verbose_name="Molarity (M)")

    def delete_row(self):
        return format_html('<i class="bi bi-trash"></i>')

    def __str__(self):
        return f"{self.inventory}: {self.type}"

    class Meta:
        verbose_name = 'Experiment Chemical'
        verbose_name_plural = 'Experiment Chemicals'


class Equipment(models.Model):

    # class Type(models.TextChoices):
    #     BATCH = 'B', 'Batch'
    #     FLOW = 'F', 'Flow'

    # id             = int, primary key, automatically provided
    serial_number = models.CharField(max_length=256)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Company, on_delete=models.CASCADE)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.serial_number

    class Meta:
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipments'


