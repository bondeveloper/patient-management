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

    path('patients/', patients, name='patients'),
    path('patients/create', create_patient, name='create_patient'),
    path('patients/<int:id>/delete', delete_patient, name='delete_patient'),
    path('patients/<int:id>/view', view_patient, name='view_patient'),
    path('patients/<int:id>/consultations/create', create_patient_consultation, name='create_patient_consultation'),
    path('patients/<int:pid>/consultations/<int:cid>/medication/create', create_patient_consultation_medication, name='create_patient_consultation_medication'),

    path('doctors/', doctors, name='doctors'),
    path('doctors/create', create_doctor, name='create_doctor'),
    path('doctors/<int:id>/delete', delete_doctor, name='delete_doctor'),
    path('doctors/<int:id>/view', view_doctor, name='view_doctor')
]
