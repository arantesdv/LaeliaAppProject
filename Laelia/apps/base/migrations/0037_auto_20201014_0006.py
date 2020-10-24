# Generated by Django 3.0.6 on 2020-10-14 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0036_auto_20201013_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Patient'),
        ),
        migrations.AlterField(
            model_name='relation',
            name='professional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Professional'),
        ),
    ]
