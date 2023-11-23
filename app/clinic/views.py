from typing import Any
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime, date
import logging
import json
from django.template.response import TemplateResponse
from django.core import serializers
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse


from clinic.models import Doctor, Patient, Appointment, Medication
from .forms import CreateDoctorModelForm, UpdateDoctorModelForm, CreatePatientModelForm, UpdateAppointmentModelForm

logger = logging.getLogger(__name__)


class UserAccessMixin(PermissionRequiredMixin):
  def dispatch(self, request, *args, **kwargs):
    if (not self.request.user.is_authenticated):
      return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
    
    if not self.has_permission():
      return redirect('/') 
    return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class CreateDoctorView(UserAccessMixin, CreateView):

  permission_required = 'clinic.add_doctor'

  model = Doctor
  form_class = CreateDoctorModelForm
  template_name = 'pages/doctors/create.html'
  success_url = '/doctors/'

  def form_valid(self, form):
    group = Group.objects.get(name='doctor') 
    form.cleaned_data['user'].groups.add(group.id)
    form.save()
    return super(CreateDoctorView, self).form_valid(form)


class UpdateDoctorView(UserAccessMixin, UpdateView):

  permission_required = 'clinic.change_doctor'

  model = Doctor
  exclude = ('user',)
  form_class = UpdateDoctorModelForm
  template_name = 'pages/doctors/create.html'
  success_url = '/doctors/'


class ListDoctorView(UserAccessMixin, ListView):

  raise_exception = False
  permission_required = 'clinic.view_doctor'
  permission_denied_message = ""
  login_url = '/signin/'
  
  model = Doctor
  template_name = 'pages/doctors/list.html'

  def get_queryset(self):
    q = self.request.GET.get('q', False)
    object_list = self.model.objects.all()
    if q:
        object_list = object_list.filter(
          Q(department__icontains=q)
          | Q(user__first_name__icontains=q)
          | Q(user__last_name__icontains=q)
          | Q(user__email__icontains=q)
          | Q(phone__icontains=q)
        )
    return object_list


def get_users(request):
  q = request.GET.get('q')
  users = get_user_model().objects.all()
  if q:
    users = users.filter(
      Q(first_name__icontains=q) |
      Q(last_name__icontains=q) |
      Q(email__icontains=q)
    )
  users_response = list(users.values())
  return JsonResponse(users_response, safe=False)

def get_doctors(request):
  q = request.GET.get('q', False)
  object_list = Doctor.objects.all()
  if q:
    object_list = object_list.filter(
      Q(phone__icontains=q) |
      Q(user__first_name__icontains=q) |
      Q(user__last_name__icontains=q) |
      Q(user__email__icontains=q)
    )
  
  data = [obj.get_doctor_user_data() for obj in object_list]
  return JsonResponse(data, safe=False)

@login_required
def delete_doctor(request, id):
  Doctor.objects.get(pk=id).delete()
  return redirect('doctors')

class CreatePatientView(UserAccessMixin, CreateView):
    
    permission_required = 'clinic.add_patient'

  
    model = Patient
    form_class = CreatePatientModelForm
    template_name = 'pages/patients/create.html'
    success_url = '/patients/'


class UpdatePatientView(UserAccessMixin, UpdateView):
    
    permission_required = 'clinic.change_patient'

    model = Patient
    form_class = CreatePatientModelForm
    template_name = 'pages/patients/create.html'
    success_url = '/patients/'


class ListPatientView(UserAccessMixin, ListView):

  raise_exception = False
  permission_required = 'clinic.view_patient'
  permission_denied_message = ""
  login_url = '/signin/'

  model = Patient
  template_name = 'pages/patients/list.html'

  def get_queryset(self):
    q = self.request.GET.get('q', False)
    object_list = self.model.objects.all()
    if q:
        object_list = object_list.filter(
          Q(first_name__icontains=q)
          | Q(last_name__icontains=q)
          | Q(email__icontains=q)
          | Q(date_of_birth__icontains=q)
          | Q(phone__icontains=q)
          | Q(gender__icontains=q)
        )
    return object_list


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

def get_patients(request):
  q = request.GET.get('q', False)
  object_list = Patient.objects.all()
  if q:
    object_list = object_list.filter(
      Q(first_name__icontains=q)
      | Q(last_name__icontains=q)
      | Q(email__icontains=q)
      | Q(gender__icontains=q)
    )
  
  patient_response = list(object_list.values())
  return JsonResponse(patient_response, safe=False)


@login_required
def delete_patient(request, id):
  Patient.objects.get(pk=id).delete()
  return redirect('patients')

class ListAppointmentView(UserAccessMixin, ListView):

  permission_required = 'clinic.view_appointment'

  model = Appointment
  template_name = 'pages/appointments/list.html'

  def get_context_data(self, **kwargs):
    appointments = Appointment.objects.all()
    context = {
        'appointments': appointments,
    }
    kwargs.update(context)
    return super().get_context_data(**kwargs)
  
  def get_queryset(self):
    q = self.request.GET.get('q', False)
    object_list = self.model.objects.all()
    if q:
        object_list = object_list.filter(
          Q(date__icontains=q)
        )
    return object_list

class UpdateAppointment(UserAccessMixin, UpdateView):
    
    permission_required = 'clinic.change_appointment'

    model = Appointment
    form_class = UpdateAppointmentModelForm
    template_name = 'pages/appointments/view.html'
    success_url = '/appointments/'

    def get_context_data(self, **kwargs):
      active_medication = Medication.objects.filter(appointment__patient=self.get_object().patient, end__gt=date.today())
      context = {
          'medications': active_medication,
      }
      kwargs.update(context)
      return super().get_context_data(**kwargs)


def create_appointment(request):
  try:
    success = True
    data = json.loads(request.body)
    doctor = Doctor.objects.get(id=data.get('id_doctor'))
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
    logger.error(e)
  return JsonResponse({'success':success})

def delete_appointment(request, id):
  Appointment.objects.get(pk=id).delete()
  return redirect('appointments')


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


# @login_required
# @permission_required('doctor.view_doctor')
# def list_doctors(request):
#   request_data = request.GET
#   filter = ''
#   if 'q' in request_data:
#     filter = request_data.get('q')
#     doctor = Doctor.objects.filter(
#       Q(user__first_name__icontains=filter)
#       | Q(user__last_name__icontains=filter)
#       | Q(phone__icontains=filter)
#       | Q(department__icontains=filter)
#     )
#   else:
#     doctor = Doctor.objects.all()
#   return render(request, 'pages/doctors/list.html', {"doctors": doctor})


# @login_required
# @require_http_methods(["GET", "POST"])
# def create_patient(request):
#   if request.method=='POST':
#     Patient.objects.create(
#       first_name=request.POST.get('first_name'),
#       last_name=request.POST.get('last_name'),
#       date_of_birth=request.POST.get('dob'),
#       email=request.POST.get('email'),
#       phone=request.POST.get('phone'),
#       gender=request.POST.get('gender'),
#       occupation=request.POST.get('occupation'),
#       street=request.POST.get('street'),
#       city=request.POST.get('city'),
#       postal_code=request.POST.get('postal_code'),
#       allergies=request.POST.get('allergies')
#     )
#     return redirect('patients')
#   return render(request, 'pages/patients/create.html', {"genders": Patient.get_genders()})

# @login_required
# @permission_required('doctor.add_doctor')
# @require_http_methods(["GET", "POST"])
# def create_doctor(request):
#   if request.method=='POST':
#     request_data = request.POST
#     user = get_user_model().objects.create_user(
#       email=request_data.get('email'),
#       password=request_data.get('password'),
#       first_name=request_data.get('first_name'),
#       last_name=request_data.get('last_name')
#     )
#     Doctor.objects.create(
#       user=user,
#       phone=request_data.get('phone'),
#       department=request_data.get('department'),
#       street=request_data.get('street'),
#       city=request_data.get('city'),
#       postal_code=request_data.get('postal_code')
#     )

#     group = Group.objects.get(name='doctor') 
#     group.user_set.add(user)
#     return redirect('doctors')
#   return render(request, 'pages/doctors/create.html')
  
# def edit_patient(request, id):
#   patient = Patient.objects.get(pk=id)
#   if request.method=='POST':
#     request_data = request.POST
#     patient.first_name = request_data.get('first_name')
#     patient.last_name = request_data.get('last_name')
#     patient.date_of_birth = request_data.get('dob')
#     patient.email = request_data.get('email')
#     patient.phone = request_data.get('phone')
#     patient.gender = request_data.get('gender')
#     patient.occupation = request_data.get('occupation')
#     patient.allergies = request_data.get('allergies')
#     patient.street = request_data.get('street')
#     patient.city = request_data.get('city')
#     patient.save()
#     return redirect('patients')
#   return render(request, 'pages/patients/edit.html', {"patient":patient, "genders": Patient.get_genders()})

# def edit_doctor(request, id):
#   doctor = Doctor.objects.get(pk=id)
#   if request.method=='POST':
#     request_data = request.POST
#     user = get_user_model().objects.get(pk=doctor.user.id)
#     user.first_name = request_data.get('first_name')
#     user.last_name = request_data.get('last_name')
#     user.email = request_data.get('email')
#     user.save()
#     doctor.phone = request_data.get('phone')
#     doctor.department = request_data.get('department')
#     doctor.postal_code = request_data.get('postal_code')
#     doctor.street = request_data.get('street')
#     doctor.city = request_data.get('city')
#     doctor.user = user
#     doctor.save()
#     return redirect('doctors')
#   return render(request, 'pages/doctors/edit.html', {"doctor":doctor})

# # DELETE
# @login_required
# @require_http_methods(["POST", "GET"])
# def view_patient_appointment(request, id, aid):
#   if request.method=='POST':
#     logger.debug("JANE")
#     appointment = Appointment.objects.get(pk=aid)
#     appointment.illness = request.POST.get('illness')
#     appointment.symptoms = request.POST.get('symptoms')
#     appointment.notes = request.POST.get('notes')
#     appointment.patient_type = request.POST.get('patient_type')
#     appointment.save()
#     return redirect('appointments_dashboard')
#   patient = Patient.objects.get(pk=id)
#   allergies = patient.allergies.split(",")
#   appointment = patient.appointment_set.get(pk=aid)
#   medications = Medication.objects.filter(appointment__patient=patient)
#   return render(request, 'pages/appointments/view.html', {
#     "patient": patient, 
#     "appointment": appointment,
#     "allergies":allergies,
#     "medications":medications
#     })

# DELETE
# @login_required
# @require_http_methods(["POST"])
# def create_patient_consultation(request, id):
#   try:
#     success = True
#     patient = Patient.objects.get(pk=id)
#     doctor = Doctor.objects.get(user=request.user)
#     data = json.loads(request.body)
#     appointment = Appointment(
#       doctor=doctor,
#       patient=patient,
#       datetime=datetime.now(),
#       **data
#     )
#     appointment.save()
#   except Exception as e:
#     success = False
#   return JsonResponse({'success':success})


# # DELETE
# @login_required
# def create_patient_consultation_medication(request, pid, cid):
#   try:
#     success=True
#     Appointment = Appointment.objects.get(pk=cid)
#     data = json.loads(request.body)
#     medication = Medication(
#       Appointment=Appointment,
#       datetime=datetime.now(),
#       **data
#     )
#     medication.save()
#   except Exception as e:
#     success = False
#     return {'e':e}
#   return JsonResponse({'success':success})

#  # Appointments

# @login_required
# def view_doctor(request, id):
#   staff = Doctor.objects.get(pk=id)
#   return render(request, 'pages/doctors/view.html', {"staff": staff})
