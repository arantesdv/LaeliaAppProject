# Generated by Django 3.0.6 on 2020-10-03 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_auto_20201003_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comercialuser',
            name='_is_active',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='comercialuser',
            name='name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]