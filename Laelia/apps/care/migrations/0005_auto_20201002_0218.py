# Generated by Django 3.0.6 on 2020-10-02 02:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('care', '0004_timelineevent_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='timelineevent',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, serialize=False),
        ),
    ]
