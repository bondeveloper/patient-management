from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime, date
import logging
import json
from django.template.response import TemplateResponse

from clinic.models import Doctor, Patient, Appointment, Medication
from .forms import AppointmentCreationForm, CreateDoctorModelForm, UpdateDoctorModelForm, CreatePatientModelForm

logger = logging.getLogger(__name__)


class CreateDoctorView(CreateView):
  model = Doctor
  form_class = CreateDoctorModelForm
  template_name = 'pages/doctors/create.html'
  success_url = '/doctors/'

class UpdateDoctorView(UpdateView):
  model = Doctor
  exclude = ('user',)
  form_class = UpdateDoctorModelForm
  template_name = 'pages/doctors/create.html'
  success_url = '/doctors/'

def get_users(request):
  if is_ajax(request=request):
    term = request.GET.get('term')
    patients = get_user_model().objects.filter(
      Q(first_name__icontains=term) |
      Q(last_name__icontains=term) |
      Q(email__icontains=term)
    )
    users_response = list(patients.values())
    return JsonResponse(users_response, safe=False)

class CreatePatientView(CreateView):
    model = Patient
    form_class = CreatePatientModelForm
    template_name = 'pages/patients/create.html'
    success_url = '/patients/'


class UpdatePatientView(UpdateView):
    model = Patient
    form_class = CreatePatientModelForm
    template_name = 'pages/patients/create.html'
    success_url = '/patients/'


@login_required
def index(request):
  return render(request, 'pages/home.html')

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
        return redirect(request.GET.get('next', 'index'))
  return render(request, 'pages/signin.html')

@login_required
def signout(request):
  logout(request)
  return redirect('signin')

@login_required
@permission_required('appointment.view_appointment')
@require_http_methods(["GET"])
def appointments_dashboard(request):
  form = AppointmentCreationForm()
  filter_date = ''
  request_data = request.GET
  if 'date' in request_data:
    filter_date = request_data.get('date')
  appointments = Appointment.objects.filter(
    Q(date__icontains=filter_date)
  )
  response_data = {
    "form": form,
    "appointments": appointments,
    "filter_date":filter_date
  }
  return render(request, 'pages/appointments/dashboard.html', response_data)


def delete_appointment(request, id):
  appointment = Appointment.objects.get(pk=id)
  appointment.delete()
  return JsonResponse({"success": True})


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

@login_required
def list_patients(request):
  request_data = request.GET
  filter = ''
  if 'q' in request_data:
    filter = request_data.get('q')
    patients = Patient.objects.filter(
      Q(first_name__icontains=filter)
      | Q(last_name__icontains=filter)
      | Q(email__icontains=filter)
      | Q(date_of_birth__icontains=filter)
      | Q(phone__icontains=filter)
    )
  else:
    patients = Patient.objects.all()
  return render(request, 'pages/patients/list.html', {"patients": patients, "filter":filter})

@login_required
@permission_required('doctor.view_doctor')
def list_doctors(request):
  request_data = request.GET
  filter = ''
  if 'q' in request_data:
    filter = request_data.get('q')
    doctor = Doctor.objects.filter(
      Q(user__first_name__icontains=filter)
      | Q(user__last_name__icontains=filter)
      | Q(phone__icontains=filter)
      | Q(department__icontains=filter)
    )
  else:
    doctor = Doctor.objects.all()
  return render(request, 'pages/doctors/list.html', {"doctors": doctor})


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
@permission_required('doctor.add_doctor')
@require_http_methods(["GET", "POST"])
def create_doctor(request):
  if request.method=='POST':
    request_data = request.POST
    user = get_user_model().objects.create_user(
      email=request_data.get('email'),
      password=request_data.get('password'),
      first_name=request_data.get('first_name'),
      last_name=request_data.get('last_name')
    )
    Doctor.objects.create(
      user=user,
      phone=request_data.get('phone'),
      department=request_data.get('department'),
      street=request_data.get('street'),
      city=request_data.get('city'),
      postal_code=request_data.get('postal_code')
    )

    group = Group.objects.get(name='doctor') 
    group.user_set.add(user)
    return redirect('doctors')
  return render(request, 'pages/doctors/create.html')
  
def edit_patient(request, id):
  patient = Patient.objects.get(pk=id)
  if request.method=='POST':
    request_data = request.POST
    patient.first_name = request_data.get('first_name')
    patient.last_name = request_data.get('last_name')
    patient.date_of_birth = request_data.get('dob')
    patient.email = request_data.get('email')
    patient.phone = request_data.get('phone')
    patient.gender = request_data.get('gender')
    patient.occupation = request_data.get('occupation')
    patient.allergies = request_data.get('allergies')
    patient.street = request_data.get('street')
    patient.city = request_data.get('city')
    patient.save()
    return redirect('patients')
  return render(request, 'pages/patients/edit.html', {"patient":patient, "genders": Patient.get_genders()})

def edit_doctor(request, id):
  doctor = Doctor.objects.get(pk=id)
  if request.method=='POST':
    request_data = request.POST
    user = get_user_model().objects.get(pk=doctor.user.id)
    user.first_name = request_data.get('first_name')
    user.last_name = request_data.get('last_name')
    user.email = request_data.get('email')
    user.save()
    doctor.phone = request_data.get('phone')
    doctor.department = request_data.get('department')
    doctor.postal_code = request_data.get('postal_code')
    doctor.street = request_data.get('street')
    doctor.city = request_data.get('city')
    doctor.user = user
    doctor.save()
    return redirect('doctors')
  return render(request, 'pages/doctors/edit.html', {"doctor":doctor})
  
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
  return render(request, 'pages/patients/view.html', {
    "patient": patient, 
    "allergies":allergies,
    "medications":medications
    })

def view_appointment(request, id):
  appointment = Appointment.objects.get(pk=id)
  if request.method=='POST':
    appointment.illness = request.POST.get('illness')
    appointment.symptoms = request.POST.get('symptoms')
    appointment.notes = request.POST.get('notes')
    appointment.patient_type = request.POST.get('patient_type')
    appointment.save()
  
  active_medication = Medication.objects.filter(appointment__patient=appointment.patient, end__gt=date.today())
  return render(request, 'pages/appointments/view.html', {
    "appointment": appointment,
    "medications":active_medication
    })

# DELETE
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
    return redirect('appointments_dashboard')
  patient = Patient.objects.get(pk=id)
  allergies = patient.allergies.split(",")
  appointment = patient.appointment_set.get(pk=aid)
  medications = Medication.objects.filter(appointment__patient=patient)
  return render(request, 'pages/appointments/view.html', {
    "patient": patient, 
    "appointment": appointment,
    "allergies":allergies,
    "medications":medications
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


def create_medication(request, id):
  try:
    success=True
    appointment = Appointment.objects.get(pk=id)
    data = json.loads(request.body)
    medication = Medication(
      appointment=appointment,
      **data
    )
    medication.save()
  except Exception as e:
    success = False
  return JsonResponse({'success':success})

# DELETE
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

@login_required
def delete_doctor(request, id):
  Doctor.objects.get(pk=id).delete()
  return redirect('doctors')

@login_required
def view_doctor(request, id):
  staff = Doctor.objects.get(pk=id)
  return render(request, 'pages/doctors/view.html', {"staff": staff})
