from datetime import date
from django.db import models
from users.models import User, Group
from chemicals.models import InChi, Name
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

class RaftAgent(models.Model):
        # id             = int, primary key, automatically provided
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'raft_agent'
        verbose_name_plural = 'raft_agents'


class QuenchingAgent(models.Model):
        # id             = int, primary key, automatically provided
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'quenching_agent'
        verbose_name_plural = 'quenching_agents'


class Solvent(models.Model):
        # id             = int, primary key, automatically provided
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'solvent'
        verbose_name_plural = 'solvents'


class Catalyst(models.Model):
        # id             = int, primary key, automatically provided
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'catalyst'
        verbose_name_plural = 'catalysts'



class Experiment(models.Model):
    # id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateField(default=date.today)
    time = models.TimeField()
    monomer = models.ForeignKey(Monomer, on_delete=models.CASCADE, default=None, blank=True, null=True)
    monomer_concentration = models.FloatField(verbose_name="Monomer Concentration", default=None, blank=True, null=True)
    
    cta = models.ForeignKey(cta, on_delete=models.CASCADE, default=None, blank=True, null=True)
    cta_concentration = models.FloatField(verbose_name="CTA concentration", default=None, blank=True, null=True)
    
    initiator = models.ForeignKey(Initiator, on_delete=models.CASCADE, default=None, blank=True, null=True, related_name='initiator')
    initiator_concentration = models.FloatField(verbose_name="Initiator Concentration", default=None, blank=True, null=True)
    
    raft_agent = models.ForeignKey(RaftAgent, on_delete=models.CASCADE, default=None, blank=True, null=True, related_name='raft_agent')
    raft_agent_concentration = models.FloatField(verbose_name="Initiator Concentration",default=None, blank=True, null=True)

    solvent = models.ForeignKey(Solvent, on_delete=models.CASCADE, default=None, blank=True, null=True, related_name='solvent')
    solvent_concentration = models.FloatField(verbose_name="Initiator Concentration", default=None, blank=True, null=True)

    catlyst = models.ForeignKey(Catalyst, on_delete=models.CASCADE, default=None, blank=True, null=True, related_name='catalyst')
    catalyst_concentration = models.FloatField(verbose_name="Initiator Concentration", default=None, blank=True, null=True)
    
    quenching_agent = models.ForeignKey(QuenchingAgent, on_delete=models.CASCADE, default=None, blank=True, null=True, related_name='quenching_agent')
    quenching_agent_concentration = models.FloatField(verbose_name="Initiator Concentration", default=None, blank=True, null=True)
    
    name = models.CharField(max_length=127, unique=True)
    temperature = models.FloatField(verbose_name="Temperature (ºC)")
    total_volume = models.FloatField(verbose_name="Volume (ml)")
    reactor = models.ManyToManyField(Reactor)
    equipment = models.ManyToManyField(Equipment)
    
    
    
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


class Experiment_Initiator(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    Initiator = models.ForeignKey(Initiator, on_delete=models.CASCADE)

class Experiment_Monomer(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    Monomner = models.ForeignKey(Monomer, on_delete=models.CASCADE)


class Experiment_Solvent(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    solvent = models.ForeignKey(Solvent, on_delete=models.CASCADE)

class Experiment_Cta(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    cta = models.ForeignKey(cta, on_delete=models.CASCADE)
    
class Experiment_Raftagent(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    raft_agent = models.ForeignKey(RaftAgent, on_delete=models.CASCADE)
class Experiment_quenchingagent(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    quenching_agent = models.ForeignKey(QuenchingAgent, on_delete=models.CASCADE)
class Experiment_Catalyst(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    catalyst = models.ForeignKey(Catalyst, on_delete=models.CASCADE)




class Reagent(models.Model):

    type = models.CharField(max_length=64)
    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Reagent'
        verbose_name_plural = 'Reagents'

from chemicals.models import CAS
class Reagent_Info(models.Model):

    name = models.CharField(max_length=128)
    reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE)
    chemical_name = models.ForeignKey(Name, on_delete=models.DO_NOTHING, null=True)


    def __str__(self):
        return f"{self.reagent}: {self.name}"

    class Meta:
        verbose_name = 'Reagent_info'
        verbose_name_plural = 'Reagents_info'

class Experiment_Reagent(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    reagent_info = models.ForeignKey(Reagent_Info, on_delete=models.CASCADE)
    concentration = models.FloatField(null=True)

    def ratios(self):
        concentrations = list(Experiment_Reagent.objects.all().values_list('concentration', flat=True))     
        min_concentration = min(concentrations)
        ratios = [i/min_concentration for i in concentrations]
        ratios = [str(i) for i in ratios]
        print(ratios)
        return(ratios)
    



    def __str__(self):
        return f"{self.experiment}: {self.reagent_info}"

    class Meta:
        verbose_name = 'Experiment_Reagent'
        verbose_name_plural = 'Experiments_Reagent'