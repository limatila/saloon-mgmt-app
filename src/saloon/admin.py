from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Client)
class ClientsAdmin(admin.ModelAdmin):
    pass
@admin.register(Worker)
class WorkersAdmin(admin.ModelAdmin):
    pass
@admin.register(Service)
class ServicesAdmin(admin.ModelAdmin):
    pass

#? intermediary tables
@admin.register(Appointment)
class AppointmentsAdmin(admin.ModelAdmin):
    list_filter = ('status', 'worker', 'service')
@admin.register(Payment)
class PaymentsAdmin(admin.ModelAdmin):
    list_filter = ('appointment', 'client')