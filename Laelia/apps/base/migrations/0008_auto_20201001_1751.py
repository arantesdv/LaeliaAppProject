# Generated by Django 3.0.6 on 2020-10-01 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20201001_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='main_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone (main)'),
        ),
        migrations.AddField(
            model_name='patient',
            name='other_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone (other)'),
        ),
        migrations.AddField(
            model_name='professional',
            name='main_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone (main)'),
        ),
        migrations.AddField(
            model_name='professional',
            name='other_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone (other)'),
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Enterprise Name')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address')),
                ('neiborhood', models.CharField(blank=True, max_length=100, null=True, verbose_name='Neiborhood')),
                ('main_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone (main)')),
                ('other_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone (other)')),
                ('notes', models.TextField(blank=True, null=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.City')),
            ],
            options={
                'verbose_name': 'Enterprise',
                'verbose_name_plural': 'Enterprises',
            },
        ),
    ]
