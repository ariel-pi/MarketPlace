# Generated by Django 5.0.4 on 2024-04-16 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0004_service_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='image',
            field=models.ImageField(default='service_images/default.jpg', upload_to='service_images'),
        ),
    ]
