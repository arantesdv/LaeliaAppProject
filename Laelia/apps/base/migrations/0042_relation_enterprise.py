# Generated by Django 3.0.6 on 2020-10-21 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0041_facility'),
    ]

    operations = [
        migrations.AddField(
            model_name='relation',
            name='enterprise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Enterprise'),
        ),
    ]