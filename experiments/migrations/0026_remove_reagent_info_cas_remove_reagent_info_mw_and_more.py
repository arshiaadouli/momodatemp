# Generated by Django 4.1.4 on 2023-08-14 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chemicals', '0002_alter_name_abbreviation_alter_name_common_name_and_more'),
        ('experiments', '0025_alter_experiment_reagent_experiment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reagent_info',
            name='cas',
        ),
        migrations.RemoveField(
            model_name='reagent_info',
            name='mw',
        ),
        migrations.AddField(
            model_name='reagent_info',
            name='inchi',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='chemicals.inchi'),
        ),
    ]
