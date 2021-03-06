# Generated by Django 3.0.6 on 2020-10-10 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meds', '0015_auto_20201010_0037'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='comercialdrug',
            name='unique_comercialdrug',
        ),
        migrations.AddConstraint(
            model_name='comercialdrug',
            constraint=models.UniqueConstraint(fields=('_name',), name='unique_comercialdrug'),
        ),
        migrations.AddConstraint(
            model_name='prescription',
            constraint=models.UniqueConstraint(fields=('comercial_drug', 'relation', 'date'), name='unique_prescription'),
        ),
    ]
