from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Parking)
admin.site.register(Car)
admin.site.register(Ticket)
admin.site.register(Bill)
admin.site.register(Payment)



