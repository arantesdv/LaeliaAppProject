# Generated by Django 3.0.6 on 2020-10-10 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meds', '0012_auto_20201010_0019'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='comercialdrug',
            constraint=models.UniqueConstraint(fields=('pt_name','total_content', 'presentation', 'dosage_form', 'volumes'), name='unique_comercialdrug'),
        ),
    ]