# Generated by Django 3.0.6 on 2020-10-10 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meds', '0016_auto_20201010_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='boxes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
