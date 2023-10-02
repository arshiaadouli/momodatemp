# Generated by Django 4.1.4 on 2023-08-03 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0022_remove_experiment_equipment_experiment_equipment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='equipment',
            field=models.ManyToManyField(to='experiments.equipment'),
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='reactor',
        ),
        migrations.AddField(
            model_name='experiment',
            name='reactor',
            field=models.ManyToManyField(to='experiments.reactor'),
        ),
    ]
