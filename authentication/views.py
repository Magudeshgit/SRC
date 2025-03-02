from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import department, User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

def signup(request):
    errortxt = ""
    if request.method == 'POST':    
        try:
            User.objects.create_user(
                username = request.POST['roll'].lower(),
                email = request.POST['personalmail'],
                collegemail = request.POST['roll'] + '@mcet.in',
                full_name = request.POST['fullname'],
                department = department.objects.get(id = int(request.POST['department'])),
                yos = request.POST['yos'],
                contact = request.POST['contact'],
                password = request.POST['password1']    
            )
            # Figure out YOS

            return redirect('/')
        except IntegrityError:
            errortxt = "User Already Exists: The entered roll no already has an account try signing in"
            
    return render(request, "authentication/signup.html", {"departments": department.objects.all().reverse(), "error": errortxt})

def signin(request):
    error = ""
    if request.method == "POST":
        auth = authenticate(request, username = request.POST['username'].lower(), password = request.POST['password'])
        if auth is not None:
            login(request, auth)
            try:
                red = request.GET['next']
                return redirect(red)
            except:
                return redirect('/')
        else:
            error = "Incorrect Username or Password"
    return render(request, "authentication/signin.html", {"error": error})

def user_logout(request):
    logout(request)
    return redirect('/')


# Password Reset
class password_reset(SuccessMessageMixin, PasswordResetView):
    template_name = 'authentication/password_reset.html'
    email_template_name = 'authentication/password_reset_mail.html'
    subject_template_name = 'authentication/password_reset_email_subject.txt'
    success_url  = reverse_lazy('passwordresetmailsent')

def passwordResetMailSent(request):
    return render(request, 'authentication/password_reset_mail_sent.html')