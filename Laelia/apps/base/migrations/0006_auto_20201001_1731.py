# Generated by Django 3.0.6 on 2020-10-01 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20201001_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='patient',
            name='main_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone (main)'),
        ),
        migrations.AddField(
            model_name='patient',
            name='neiborhood',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Neiborhood'),
        ),
        migrations.AddField(
            model_name='patient',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='other_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone (other)'),
        ),
        migrations.AddField(
            model_name='professional',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='professional',
            name='main_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone (main)'),
        ),
        migrations.AddField(
            model_name='professional',
            name='neiborhood',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Neiborhood'),
        ),
        migrations.AddField(
            model_name='professional',
            name='other_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone (other)'),
        ),
    ]