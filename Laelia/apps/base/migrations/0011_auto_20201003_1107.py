# Generated by Django 3.0.6 on 2020-10-03 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0010_relation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='professional',
            options={'permissions': [('inactivate_professional', 'Can inactivate the professional.'), ('assist_professional', 'Can assist the professional.')], 'verbose_name': 'Professional', 'verbose_name_plural': 'Professionals'},
        ),
        migrations.AddField(
            model_name='patient',
            name='_is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='professional',
            name='_is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AddField(
            model_name='professional',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
