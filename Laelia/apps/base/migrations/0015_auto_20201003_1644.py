# Generated by Django 3.0.6 on 2020-10-03 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_auto_20201003_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprise',
            name='professionals',
            field=models.ManyToManyField(related_name='enterprise_professionals', to='base.Professional'),
        ),
    ]
