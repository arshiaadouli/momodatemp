# Generated by Django 4.1.4 on 2023-07-12 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0002_cta_monomer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='cta',
        ),
        migrations.DeleteModel(
            name='Monomer',
        ),
    ]