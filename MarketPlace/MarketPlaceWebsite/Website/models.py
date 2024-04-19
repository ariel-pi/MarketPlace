# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # this is optional, you can add a profile picture
    # profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Service(models.Model):
    # this is optional, you can use the default map location or add your own
    # DEFAULT_MAP_LOCATION = r"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3487844.11496039!2d32.44041769453558!3d31.383867609568092!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x1500492432a7c98b%3A0x6a6b422013352cba!2sIsrael!5e0!3m2!1sen!2sil!4v1712740457423!5m2!1sen!2sil"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opening_time = models.TimeField(default='10:00:00')
    closing_time = models.TimeField(default='18:00:00')
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    # this is optional, you can use the default map location or add your own
    # map_location = models.URLField(default=DEFAULT_MAP_LOCATION, max_length=1000)
    contact_details = models.CharField(max_length=255)
    available_spaces = models.PositiveIntegerField()
    image = models.ImageField(upload_to='service_images', default='service_images/default.jpg')

    def __str__(self):
        return self.name



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.service.name} ({self.rating})"

class ServiceItem(models.Model):
    identifier = models.CharField(primary_key=True, max_length=50, unique=True, verbose_name="identifier")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner")
    description = models.CharField(max_length=20, verbose_name="item's name")
    field_1 = models.CharField(max_length=80, verbose_name="field 1")
    field_2 = models.IntegerField(verbose_name="field 2")
    FIELD_3_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No')
    ]
    field_3 = models.CharField(max_length=3, choices=FIELD_3_CHOICES, verbose_name="field 3", help_text="User type selection (yes/no)")



    def __str__(self):
        return self.description+ ", id:"+self.identifier
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    # change this if you want to change the available hours


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service,  on_delete=models.SET_NULL, null=True)
    # optional fields
    # check_in_date = models.DateField()
    # check_out_date = models.DateField()

    date = models.DateField(default=timezone.now) 
    time = models.TimeField( default='10:00:00')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    service_provider_notes = models.TextField(blank=True, null=True)
    client_notes = models.TextField(blank=True, null=True)
    service_item = models.ForeignKey(ServiceItem, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.service.name} ({self.status})"
