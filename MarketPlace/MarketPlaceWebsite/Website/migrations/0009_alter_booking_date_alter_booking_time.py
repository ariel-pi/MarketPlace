# Generated by Django 5.0.4 on 2024-04-19 13:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0008_booking_date_alter_booking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='booking',
            name='time',
            field=models.TimeField(choices=[('9:00:00', '9:00:00'), ('10:00:00', '10:00:00'), ('11:00:00', '11:00:00'), ('12:00:00', '12:00:00'), ('13:00:00', '13:00:00'), ('14:00:00', '14:00:00'), ('15:00:00', '15:00:00'), ('16:00:00', '16:00:00')], default='9:00'),
        ),
    ]
