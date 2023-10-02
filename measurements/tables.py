from cgitb import html
from django_tables2 import tables, TemplateColumn
# from django_tables2.columns import LinkColumn 
from .models import Measurement
from experiments.models import Monomer


class MeasurementTable(tables.Table):

    class Meta:
        model = Measurement
        attrs = {'class': 'table', 'td': {'class': 'align-middle'}}
        fields = ['file', 'device', 'delete']
        attrs = {"class": "table table-hover"}
        # row_attrs = {"onClick": lambda record: "document.location.href='/add-csv-data/{0}';".format(record.id)}  

    delete = TemplateColumn(template_name='measurements/delete_file_button.html',
                            verbose_name='', attrs={'td': {'align': 'right'}})

    # file = tables.LinkColumn(
    #     'measurement_file',  # URL name for the details page
    #     args=[tables.A('id')],  # Pass the ID as an argument to the URL
    #     verbose_name='file'  # Display name for the link
    # )

class MonomerTable(tables.Table):
    class Meta:
        model = Monomer
        fields = ("name", )
        attrs = {"class": "table table-hover"}
        # row_attrs = {
        #     "onClick": lambda record: "document.location.href='/measurements/view_3d_monomer_graph/{0}';".format(record.name)}
    delete = TemplateColumn(template_name='measurements/view3d.html',
                            verbose_name='3D VIEW')
    kinetics = TemplateColumn(template_name='measurements/view_kinetic_values_graph.html',
                              verbose_name='Kinetic VIEW')
