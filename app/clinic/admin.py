from django.contrib import admin
from clinic.models import Patient, Doctor, Consultation, Medication

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Consultation)
admin.site.register(Medication)
