# Generated by Django 3.0.6 on 2020-10-04 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_enterprise_sponsor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(auto_created=True)),
                ('duration', models.IntegerField(choices=[(900, '15 MIN'), (1800, '30 MIN'), (2700, '45 MIN'), (3600, '60 MIN')], default=2700)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
