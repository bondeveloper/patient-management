from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from clinic.models import Doctor, Patient, Appointment, Medication
from django.http import HttpResponse, JsonResponse
import json
from datetime import datetime
from django.core import serializers

def index(request):
  return redirect('patients')


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
        return redirect(request.GET.get('next', 'patients'))
  return render(request, 'pages/signin.html')

@login_required
def signout(request):
  logout(request)
  return redirect('/')

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
  consultations = Appointment.objects.filter(patient=patient)
  medications = Medication.objects.filter(consultation__patient=patient)
  return render(request, 'pages/patients/view.html', {
    "patient": patient, 
    "types": Appointment.get_patient_types(),
    "consultations": consultations,
    "medications": medications,
    "allergies":allergies
    })

@login_required
@require_http_methods(["POST"])
def create_patient_consultation(request, id):
  try:
    success = True
    patient = Patient.objects.get(pk=id)
    doctor = Doctor.objects.get(user=request.user)
    data = json.loads(request.body)
    Appointment = Appointment(
      doctor=doctor,
      patient=patient,
      datetime=datetime.now(),
      **data
    )
    Appointment.save()
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
