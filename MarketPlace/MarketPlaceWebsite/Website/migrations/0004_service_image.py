# Generated by Django 5.0.4 on 2024-04-16 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0003_remove_service_map_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='service_images'),
        ),
    ]
