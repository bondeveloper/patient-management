from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from clinic.models import MedicalStaff, Patient
from django.http import HttpResponse

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

@login_required
def patients(request):
  patients = Patient.objects.all()
  return render(request, 'pages/patient/list.html', {"patients": patients})

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
      postal_code=request.POST.get('postal_code')
    )
    return redirect('patients')
  return render(request, 'pages/patient/create.html', {"genders": Patient.get_genders()})

@login_required
def delete_patient(request, id):
  Patient.objects.get(pk=id).delete()
  return redirect('patients')

@login_required
def view_patient(request, id):
  patient = Patient.objects.get(pk=id)
  return render(request, 'pages/patient/view.html', {"patient": patient})

@login_required
def medical_staff(request):
  staff = MedicalStaff.objects.all()
  return render(request, 'pages/medical_staff/list.html', {"data": staff})

@login_required
@require_http_methods(["GET", "POST"])
def create_medical_staff(request):
  if request.method=='POST':
    MedicalStaff.objects.create(
      user=get_user_model().objects.get(pk=request.POST.get('user')),
      phone=request.POST.get('phone'),
      position=request.POST.get('position'),
      department=request.POST.get('department'),
      street=request.POST.get('street'),
      city=request.POST.get('city'),
      postal_code=request.POST.get('postal_code')
    )
    return redirect('medical_staff')
  users = get_user_model().objects.all()
  return render(request, 'pages/medical_staff/create.html', {"users": users, "positions": MedicalStaff.get_positions()})

@login_required
def delete_medical_staff(request, id):
  MedicalStaff.objects.get(pk=id).delete()
  return redirect('medical_staff')

@login_required
def view_medical_staff(request, id):
  staff = MedicalStaff.objects.get(pk=id)
  return render(request, 'pages/medical_staff/view.html', {"staff": staff})
