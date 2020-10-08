# Generated by Django 3.0.6 on 2020-10-05 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_auto_20201003_2233'),
        ('meds', '0008_auto_20201005_0625'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='relation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Relation'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='dosage_regimen',
            field=models.IntegerField(choices=[(1, '1x'), (2, '2x'), (3, '3x'), (4, '4x'), (5, '5x'), (6, '6x'), (7, '7x'), (8, '8x'), (9, '9x'), (10, '10x'), (11, '11x'), (12, '12x')], default=1),
        ),
    ]
