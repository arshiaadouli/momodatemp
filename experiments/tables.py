import django_tables2 as tables
from .models import Experiment, Experiment_Chemicals, Reactor, Inventory, Equipment, Experiment_Reagent
# from django_tables2 import tables, TemplateColumn
class ExperimentTable(tables.Table):
    class Meta:
        model = Experiment
        fields = ("user", "name", "temperature", "total_volume", "reactor", )
        attrs = {"class": "table table-hover"}
        row_attrs = {"onClick": lambda record: "document.location.href='/experiments/my_experiments/{0}/0';".format(record.id)}       #URL is not dynamic here

class SupplierTable(tables.Table):
    class Meta:
        model = Inventory
        fields = ("inchi", "company", "purity", )
        #attrs = {"class": "table table-hover"}    #disabled while not clickable

class SuppliesTable(tables.Table):


    class Meta:
        model = Experiment
        fields = ("name", "temperature", "reactor", "total_volume")

class ReactorTable(tables.Table):
    class Meta:
        model = Reactor
        fields = ("name", "volume", "type")
        #attrs = {"class": "table table-hover"}    #disabled while not clickable

class EquipmentTable(tables.Table):
    class Meta:
        model = Equipment
        fields = ("group", "vendor", "serial_number", "details")
        #attrs = {"class": "table table-hover"}    #disabled while not clickable

class ArrayColumn(tables.Column):
    def __init__(self, index, *args, **kwargs):
        self.index = index
        super(ArrayColumn, self).__init__(*args, **kwargs)

    def render(self, value, record, **kwargs):
        if value is None or len(value) <= self.index:
            return ''
        return str(value[self.index])

class ExperimentReagentTable(tables.Table):

    class Meta:
        model = Experiment_Reagent
        fields = ('reagent_info', 'concentration', 'ratio')
        attrs = {"class": "table table-hover"}    #disabled while not clickable