from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from clinic.models import Doctor, Patient, Appointment, Medication
from django.http import HttpResponse, JsonResponse
import json
from datetime import datetime, date
from django.core import serializers
from django.views.generic import ListView, FormView
from django.db.models import Q
from .forms import AppointmentCreationForm
import logging

logger = logging.getLogger(__name__)


class PatientListView(ListView):
  model = Patient
  template_name = 'pages/appointment_list.html'

  def get_queryset(self) -> QuerySet[Any]:
    query = self.request.GET.get('patient')
    return Patient.objects.filter(
      Q(first_name__icontains=query) | 
      Q(last_name__icontains=query) 
    )


def index(request):
  return redirect('dashboard')


@require_http_methods(["GET", "POST"])
def signin(request):
  if request.method=='POST':
    user = authenticate(
      request,
      email=request.POST.get('email'),
      password=request.POST.get('password')
    )

    if user is not None:
        login(request, user)
        return redirect(request.GET.get('next', 'dashboard'))
  return render(request, 'pages/signin.html')

@login_required
def signout(request):
  logout(request)
  return redirect('/')

@login_required
@require_http_methods(["GET"])
def dashboard(request):
  form = AppointmentCreationForm()
  # TODO check user type and render relevant dashboard. for now will default to doctor
  filter_date = date.today()
  key = ""
  request_data = request.GET
  if 'key' in request_data:
    filter_date = request.GET.get('date')
    key = request.GET.get('key')
  appointments = Appointment.objects.filter(
        # Q(date__icontains=date) |
        Q(patient__first_name__icontains=key) |
        Q(patient__last_name__icontains=key) |
        Q(patient__email__icontains=key)
      )
  response_data = {
    "form": form,
    "appointments": appointments,
    "filter":filter_date
  }
  return render(request, 'pages/doctors/dashboard.html', response_data)

def get_patients(request):
  if is_ajax(request=request):
    term = request.GET.get('term')
    patients = Patient.objects.filter(
      Q(first_name__icontains=term) |
      Q(last_name__icontains=term) |
      Q(email__icontains=term)
    )
    patient_response = list(patients.values())
    return JsonResponse(patient_response, safe=False)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# PATIENTS
@login_required
def patients(request):
  patients = Patient.objects.all()
  return render(request, 'pages/patients/list.html', {"patients": patients})

@login_required
@require_http_methods(["GET", "POST"])
def create_patient(request):
  if request.method=='POST':
    Patient.objects.create(
      first_name=request.POST.get('first_name'),
      last_name=request.POST.get('last_name'),
      date_of_birth=request.POST.get('dob'),
      email=request.POST.get('email'),
      phone=request.POST.get('phone'),
      gender=request.POST.get('gender'),
      occupation=request.POST.get('occupation'),
      street=request.POST.get('street'),
      city=request.POST.get('city'),
      postal_code=request.POST.get('postal_code'),
      allergies=request.POST.get('allergies')
    )
    return redirect('patients')
  return render(request, 'pages/patients/create.html', {"genders": Patient.get_genders()})

@login_required
def delete_patient(request, id):
  Patient.objects.get(pk=id).delete()
  return redirect('patients')

@login_required
def view_patient(request, id):
  patient = Patient.objects.get(pk=id)
  allergies = patient.allergies.split(",")
  appointments = patient.appointment_set.all()
  medications = Medication.objects.filter(appointment__patient=patient)
  active_medication = medications.filter(end__gt=datetime.now())
  return render(request, 'pages/patients/view.html', {
    "patient": patient, 
    "types": Appointment.get_patient_types(),
    "appointments": appointments,
    "allergies":allergies,
    "active_medications":active_medication
    })

@login_required
@require_http_methods(["POST", "GET"])
def view_patient_appointment(request, id, aid):
  if request.method=='POST':
    logger.debug("JANE")
    appointment = Appointment.objects.get(pk=aid)
    appointment.illness = request.POST.get('illness')
    appointment.symptoms = request.POST.get('symptoms')
    appointment.notes = request.POST.get('notes')
    appointment.patient_type = request.POST.get('patient_type')
    appointment.save()
    return redirect('dashboard')
  patient = Patient.objects.get(pk=id)
  allergies = patient.allergies.split(",")
  appointment = patient.appointment_set.get(pk=aid)
  medications = Medication.objects.filter(appointment__patient=patient)
  active_medication = medications.filter(end__gt=datetime.now())
  return render(request, 'pages/appointments/view.html', {
    "patient": patient, 
    "types": Appointment.get_patient_types(),
    "appointment": appointment,
    "allergies":allergies,
    "active_medications":active_medication
    })

# DELETE
@login_required
@require_http_methods(["POST"])
def create_patient_consultation(request, id):
  try:
    success = True
    patient = Patient.objects.get(pk=id)
    doctor = Doctor.objects.get(user=request.user)
    data = json.loads(request.body)
    appointment = Appointment(
      doctor=doctor,
      patient=patient,
      datetime=datetime.now(),
      **data
    )
    appointment.save()
  except Exception as e:
    success = False
  return JsonResponse({'success':success})

@login_required
def create_patient_consultation_medication(request, pid, cid):
  try:
    success=True
    Appointment = Appointment.objects.get(pk=cid)
    data = json.loads(request.body)
    medication = Medication(
      Appointment=Appointment,
      datetime=datetime.now(),
      **data
    )
    medication.save()
  except Exception as e:
    success = False
    return {'e':e}
  return JsonResponse({'success':success})

 # Appointments

@login_required
def doctor_appointments_create(request):
  try:
    success = True
    doctor = Doctor.objects.get(user=request.user)
    data = json.loads(request.body)
    patient = Patient.objects.get(pk=data.get('id_patient'))
    appointment = Appointment(
      doctor=doctor,
      patient=patient,
      date=data.get('date'),
      time=data.get('time'),
    )
    appointment.save()
  except Exception as e:
    success = False
    logger.error(e.args[0])
  return JsonResponse({'success':success})


# DOCTORS

@login_required
def doctors(request):
  staff = Doctor.objects.all()
  return render(request, 'pages/doctors/list.html', {"data": staff})

@login_required
@require_http_methods(["GET", "POST"])
def create_doctor(request):
  if request.method=='POST':
    Doctor.objects.create(
      user=get_user_model().objects.get(pk=request.POST.get('user')),
      phone=request.POST.get('phone'),
      position=request.POST.get('position'),
      department=request.POST.get('department'),
      street=request.POST.get('street'),
      city=request.POST.get('city'),
      postal_code=request.POST.get('postal_code')
    )
    return redirect('doctors')
  users = get_user_model().objects.all()
  return render(request, 'pages/doctors/create.html', {"users": users})

@login_required
def delete_doctor(request, id):
  Doctor.objects.get(pk=id).delete()
  return redirect('doctors')

@login_required
def view_doctor(request, id):
  staff = Doctor.objects.get(pk=id)
  return render(request, 'pages/doctors/view.html', {"staff": staff})
