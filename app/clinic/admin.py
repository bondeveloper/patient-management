from django.contrib import admin
from clinic.models import Patient, Doctor, Appointment, Medication

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
  list_display = ('first_name', 'last_name', 'phone')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
  list_display = ('user', 'phone', 'department')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
  list_display = ('patient', 'date', 'time')
# Register your models here.
# admin.site.register(Patient, PatientAdmin)
# admin.site.register(Doctor)
# admin.site.register(Appointment)
# admin.site.register(Medication)

