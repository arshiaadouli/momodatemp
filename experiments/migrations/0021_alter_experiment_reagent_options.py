# Generated by Django 4.1.4 on 2023-08-03 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0020_experiment_reagent_concentration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='experiment_reagent',
            options={'verbose_name': 'Experiment_Reagent', 'verbose_name_plural': 'Experiments_Reagent'},
        ),
    ]
