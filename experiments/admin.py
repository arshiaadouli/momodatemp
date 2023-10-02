import imp
from django.contrib import admin

from .models import *

class ReactorConfig(admin.ModelAdmin):

    list_display = ('name', 'volume', 'type')

admin.site.register(Reactor, ReactorConfig)

class CompanyConfig(admin.ModelAdmin):

    list_display = ('name',)

admin.site.register(Company, CompanyConfig)

class ExperimentConfig(admin.ModelAdmin):

    list_display = ('user_id', 'date', 'time', 'name', 'temperature', 'total_volume', 'reactor_id')

admin.site.register(Experiment)

class InventoryConfig(admin.ModelAdmin):

    list_display = ('company', 'inchi', 'purity')

admin.site.register(Inventory, InventoryConfig)

class ExperimentChemicalsConfig(admin.ModelAdmin):

    list_display = ('experiment', 'inventory', 'type', 'molarity')

admin.site.register(Experiment_Chemicals, ExperimentChemicalsConfig)
admin.site.register(Initiator)
admin.site.register(Equipment)

admin.site.register(QuenchingAgent)
admin.site.register(RaftAgent)
admin.site.register(Catalyst)
admin.site.register(Solvent)
admin.site.register(cta)

admin.site.register(Reagent)
admin.site.register(Reagent_Info)
admin.site.register(Experiment_Reagent)