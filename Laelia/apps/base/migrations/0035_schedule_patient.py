# Generated by Django 3.0.6 on 2020-10-12 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0034_auto_20201011_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Patient'),
        ),
    ]
