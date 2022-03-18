from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from eDoc.models import Specialization, Doctor, Patient
from django.db.models import Q


@login_required(login_url='/login/')
def index(request):
    user = request.user
    specialization = Specialization.objects.all()
    doctors = Doctor.objects.all()
    context = {'specializations': specialization, 'doctors': doctors, 'user': user}

    return render(request, 'home.html', context=context)

@login_required(login_url='/login/')
def docindex(request):
    user = request.user
    specialization = Specialization.objects.all()

    doctor = Doctor.objects.get(user=user)
    context = {'specializations': specialization, 'doctor': doctor, 'user': user}

    return render(request, 'DocHome.html', context=context)


def search(request):
    print("inside search function in view")
    specializations = Specialization.objects.all()
    doctors = []
    user = request.user
    if request.method == "POST":
        special = request.POST.get('selSpecialization')

        name = request.POST.get('docName')
        if name:
            doctors = Doctor.objects.filter(Q(name__contains=name) | Q(specialization__name=special))
        else:
            doctors = Doctor.objects.filter(Q(specialization__name=special))

    context = {'doctors': doctors, 'specializations': specializations, 'user': user}

    return render(request, 'home.html', context=context)


def validate_username(request):
    print('inside validate user')
    username = request.GET.get('username', None)

    print(username)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def registerPatient(request):
    if request.method == "POST":
        name = request.POST.get('patientname')
        email = request.POST.get('patientemail')
        password = request.POST.get('patientpassword')
        contactNo = request.POST.get('patientContactNo')

        if User.objects.filter(username__iexact=email).exists():
            return render(request, 'registerPatient.html', )

        user = User.objects.create_user(username=email, first_name=name, email=email, password=password)
        user.save()
        patient = Patient.objects.create(user=user, name=name, contact=contactNo)
        patient.save()
        loguser = authenticate(username=email, password=password)

        if loguser is not None:
            login(request, loguser)
            return redirect('index')

    userdata = Patient.objects.last()
    context = {'userdata': userdata}

    return render(request, 'registerPatient.html', context=context)


def registerDoctor(request):
    specializations = Specialization.objects.all()
    context = {'specializations': specializations}
    if request.method == "POST":
        name = request.POST.get('doctorname')
        email = request.POST.get('doctoremail')
        password = request.POST.get('doctorpassword')
        contactNo = request.POST.get('doctorContactNo')
        address = request.POST.get('doctoraddress')
        special = request.POST.get('selSpecialization')
        picture = request.FILES["docpicture"]
        if User.objects.filter(username__iexact=email).exists():
            return render(request, 'registerDoctor.html', context=context)

        user = User.objects.create_user(username=email, first_name=name, email=email, password=password)
        user.save()
        docspecialization = Specialization.objects.get(name__exact=special)
        doctor = Doctor.objects.create(user=user, name=name, contact=contactNo, specialization=docspecialization,
                                       address=address, picture=picture, email=email)
        doctor.save()
        loguser = authenticate(username=email, password=password)

        if loguser is not None:
            login(request, loguser)
            return redirect('docindex')

    userdata = Patient.objects.last()

    context = {'specializations': specializations, 'userdata': userdata}

    return render(request, 'registerDoctor.html', context=context)


def login_user(request):
    print('inside login')
    if request.method == "POST":

        username = request.POST['loginEmail']
        password = request.POST['loginpassword']

        print("inside post in  login form", username, password)
        user = authenticate(username=username, password=password)

        print(user)
        if user is not None:
            login(request, user)
            if patient_exist(user):
                return redirect('index')
            else:
                return redirect('docindex')
        else:
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout_user(request):
    print("inside logout ")
    logout(request)
    return redirect('login')


def patient_exist(user):
    return Patient.objects.filter(user__exact=user).exists()
