from django.contrib import admin
from clinic.models import Patient, Doctor, Appointment, Medication

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Medication)
