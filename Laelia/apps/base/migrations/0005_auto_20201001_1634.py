# Generated by Django 3.0.6 on 2020-10-01 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20201001_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professional',
            name='aditional_info',
        ),
        migrations.AddField(
            model_name='professional',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
