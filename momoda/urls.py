from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users.views import staff_info, home_page, my_account, research_group, create_group, get_institution_ajax
from chemicals.views import search_chemicals, add_chemical, chemical_details
from experiments.views import *
from chemicals.views import add_reagent_info
from measurements.views import monomer_kinetics, upload_file, delete_file, view_3d_graph, view_graph, view_3d_kinetic_graph, monomer_models, all_visualisations, delete_supply
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('', home_page, name='home'),
    path('staff_info/', staff_info, name='staff_info'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/me', my_account, name='my_account'),
    path('groups/create', create_group, name='create_group'),
    path('groups/ajax', get_institution_ajax, name='get_institution_ajax'),
    path('groups/<int:pk>', research_group, name='research_group'),
    path('monomers/', search_chemicals, name='search_chemicals'),
    path('monomers/add', add_chemical, name='add_chemical'),
    path('monomers/<int:pk>', chemical_details, name='chemical_details'),
    path('experiments/my_experiments', my_experiments, name="my_experiments"),
    path('experiments/my_experiments/add',
         add_experiment, name="add_experiment"),
    path('experiments/my_experiments/<int:pk>/<int:error>',
         experiment_detail, name="experiment_detail"),
    path('experiments/my_chemicals', my_chemicals, name="my_chemicals"),
    path('measurements/monomer_kinetics',
         monomer_kinetics, name="monomer_kinetics"),
    path('experiments/my_chemicals/add', add_supplier, name="add_supplier"),
    path('experiments/my_reactors', my_reactors, name="my_reactors"),
    path('experiments/reactor/add', add_reactor, name="add_reactor"),
    path('experiments/equipments', equipments, name='equipments'),
    path('experiments/equipments/add', insert_equipment, name='insert_equipment'),
    path('measurements/upload/<int:pk>', upload_file, name="upload_file"),
    path('measurements/delete/<int:pk>/<int:path>',
         delete_file, name="delete_file"),
    path('measurements/graph/<int:pk>', view_graph, name='view_graph'),
    path('measurements/view_3d_monomer_graph/<str:name>',
         view_3d_graph, name='view_3d_monomer_graph'),
    path('measurements/view_3d_kinetics_graph/<str:name>',
         view_3d_kinetic_graph, name='view_3d_kinetic_graph'),
    path('measurements/monomer_models/',
         monomer_models, name='monomer_models'),
    path('measurements/all_visualisations/',
         all_visualisations, name='all_visualisations'),
    path('measurements/delete/supply/<int:pk>/<int:path>',
         delete_supply, name='delete_supply'),
     path('experiment-test',
         experiment_test, name='experiment_test'),

     path('delete-reagent/<int:object_id>/',
         delete_reagent, name='delete-reagent'),

     path('delete-experiment/<int:object_id>/',
         delete_experiment, name='delete-experiment'),

     path('delete-data/<int:item>/<int:fk>',
         delete_data, name='delete-data'),

     
     path('edit-data/<int:pk>/<int:fk>',
         edit_data, name='edit-data'),

     path('edit-experiment/<int:item_id>/',
         edit_experiment, name='edit-experiment'),

     path('edit-experiment/<int:item_id>/',
         edit_experiment, name='edit-experiment'),

     path('add-reagent-info/', add_reagent_info, name='add_reagent_info'),
     path('add-reagent-info/<int:chemical_id>', add_reagent_info, name='add_reagent_info_chemical'),

     path('add-csv-data/<int:pk>', add_csv_data, name='add_csv_data')

]


urlpatterns+= staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
