# Generated by Django 3.0.6 on 2020-10-03 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_auto_20201003_1917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comercialuser',
            name='employees',
        ),
        migrations.RemoveField(
            model_name='comercialuser',
            name='enterprises',
        ),
        migrations.RemoveField(
            model_name='comercialuser',
            name='professionals',
        ),
        migrations.AddField(
            model_name='comercialuser',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='comercialuser',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.City'),
        ),
        migrations.AddField(
            model_name='comercialuser',
            name='main_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone (main)'),
        ),
        migrations.AddField(
            model_name='comercialuser',
            name='neiborhood',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Neiborhood'),
        ),
        migrations.AddField(
            model_name='comercialuser',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comercialuser',
            name='other_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone (other)'),
        ),
        migrations.AddField(
            model_name='employee',
            name='sponsor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.ComercialUser'),
        ),
        migrations.AddField(
            model_name='professional',
            name='sponsor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.ComercialUser'),
        ),
    ]