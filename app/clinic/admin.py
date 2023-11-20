from django.contrib import admin
from clinic.models import Patient, Doctor, Appointment, Medication

class PatientAdmin(admin.ModelAdmin):
  list_display = ('first_name', 'last_name', 'phone')


# Register your models here.
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Medication)
