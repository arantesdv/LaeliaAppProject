# Generated by Django 3.0.6 on 2020-10-14 03:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0037_auto_20201014_0006'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ComercialUser',
            new_name='Sponsor',
        ),
    ]
