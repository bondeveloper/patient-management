"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from clinic.views import *

urlpatterns = [
    
    path('', index, name='index'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),

    path('api/patients/', get_patients, name='get_patients'),
    path('api/appointments/<int:id>/medication/create', create_medication, name='create_medication'),

    path('appointments/', ListAppointmentView.as_view(), name='appointments_dashboard'),
    path('appointments/<int:pk>/view', UpdateAppointment.as_view(), name='view_appointment'),
    path('appointments/<int:id>/delete', delete_appointment, name='delete_appointment'),
    path('api/appointments/create', create_appointment, name='create_appointment'),

    path('patients/', ListPatientView.as_view(), name='patients'),
    path('patients/create', CreatePatientView.as_view(), name='create_patient'),
    path('patients/<int:pk>/edit', UpdatePatientView.as_view(), name='edit_patient'),
    path('patients/<int:id>/delete', delete_patient, name='delete_patient'),
    path('patients/<int:id>/view', view_patient, name='view_patient'),

    path('doctors/', ListDoctorView.as_view(), name='doctors'),
    path('doctors/create', CreateDoctorView.as_view(), name='create_doctor'),
    path('doctors/<int:pk>/edit', UpdateDoctorView.as_view(), name='edit_doctor'),
    path('doctors/<int:id>/delete', delete_doctor, name='delete_doctor'),
    path('api/users/', get_users, name='get_users'),
    path('api/doctors/', get_doctors, name='get_doctors'),

]
