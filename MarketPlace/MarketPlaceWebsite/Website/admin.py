# admin.py

from django.contrib import admin
from .models import  Service, Booking ,Profile, Review, ServiceItem

admin.site.register(Profile)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(ServiceItem)
