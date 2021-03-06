# Generated by Django 3.0.6 on 2020-10-22 16:46

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0042_relation_enterprise'),
        ('care', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalLicence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modification Date and Time')),
                ('_is_ongoing', models.BooleanField(default=True, editable=False)),
                ('_is_protected', models.BooleanField(default=False, editable=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('from_date', models.DateField(blank=True, null=True)),
                ('from_time', models.TimeField(blank=True, null=True)),
                ('to_time', models.TimeField(blank=True, null=True)),
                ('to_date', models.DateField(blank=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('introduction', models.TextField(blank=True, null=True)),
                ('discussion', models.TextField(blank=True, null=True)),
                ('conclusion', models.TextField(blank=True, null=True)),
                ('disability_type', models.CharField(blank=True, choices=[('permanent disability', 'permanent disability'), ('temporary disability', 'temporary disability')], max_length=50, null=True)),
                ('leave_days', models.IntegerField()),
                ('relation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Relation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
