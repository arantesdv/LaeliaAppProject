# Generated by Django 3.0.6 on 2020-10-10 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meds', '0011_auto_20201008_1257'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='compoundset',
            constraint=models.UniqueConstraint(fields=('active_compound', 'strength_value', 'strength_measure_unit'), name='unique_compoundset'),
        ),
    ]