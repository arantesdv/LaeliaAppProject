# Generated by Django 3.0.6 on 2020-10-05 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meds', '0004_auto_20201004_2328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comercialdrug',
            name='box_content',
        ),
        migrations.AddField(
            model_name='comercialdrug',
            name='total_content',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comercialdrug',
            name='volumes',
            field=models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=1, null=True),
        ),
        migrations.CreateModel(
            name='PrescriptionMixin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modification Date and Time')),
                ('_is_ongoing', models.BooleanField(default=True, editable=False)),
                ('_is_protected', models.BooleanField(default=False, editable=False)),
                ('comercial_drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meds.ComercialDrug')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
