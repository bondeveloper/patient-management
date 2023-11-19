from django.contrib import admin
from clinic.models import Patient, MedicalStaff

# Register your models here.
admin.site.register(Patient)
admin.site.register(MedicalStaff)
