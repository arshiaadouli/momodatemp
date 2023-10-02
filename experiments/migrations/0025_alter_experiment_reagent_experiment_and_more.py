# Generated by Django 4.1.4 on 2023-08-09 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chemicals', '0002_alter_name_abbreviation_alter_name_common_name_and_more'),
        ('experiments', '0024_alter_experiment_catalyst_catalyst_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment_reagent',
            name='experiment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiments.experiment'),
        ),
        migrations.AlterField(
            model_name='experiment_reagent',
            name='reagent_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiments.reagent_info'),
        ),
        migrations.AlterField(
            model_name='reagent_info',
            name='cas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chemicals.cas'),
        ),
        migrations.AlterField(
            model_name='reagent_info',
            name='reagent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiments.reagent'),
        ),
    ]