from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .emailBackend import EmailBackend
# from django.contrib.auth.forms import PasswordResetForm,
from .forms import passwordResetForm, changePasswordForm
from django.db.models import Q
# Create your views here.
#
#password reset
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


def registrationView(request):
    # user = User.objects.all()

    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        username = request.POST['username']
        print('**************===========================')
        print(request.POST)

        #check if username exists
        if User.objects.filter(username = username).exists():
            messages.warning(request, f"the username <b>{username}</b> already exists!")
            return redirect('register')
        #check if email already exists

        if User.objects.filter(email = email ).exists():
            messages.warning(request, f'the email: <b>{email}</b> has been taken already!')
            return redirect('register')
        
        if password1 != password2:
            messages.info(request, 'password does not match')
            return redirect('register')

        user = User.objects.create_user(username = username, email = email)
        user.set_password(password1)
        user.save()
        messages.success(request, f'welcome  <b>{user.username}! You can now login')
        return redirect('login')
      

    return render(request, 'accounts/register.html')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = EmailBackend.authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'accounts/login.html')

def logoutView(request):
    if (request.method == 'POST' or request.method == 'GET'):
        logout(request)
        messages.info(request, 'You have logged out')
        return redirect('home')
    messages.info(request, 'You have NOT logged out')
    return redirect('/')


def resetPassword(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = passwordResetForm(data=request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = User.objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('/')
        

        for key, error in list(form.errors.items()):
            messages.error(request,  error)
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                
        
                



    form = passwordResetForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/password_reset_form.html', context)


def passwordResetConfirmation(request, uidb64, token):

    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = changePasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('/')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = changePasswordForm(user)
        context = {
            'form':form
        }
        return render(request, 'accounts/password_reset_confirm.html', context)
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("/")


def resetPasswordDone(request):
    pass

def resetPasswordConfirm(request):
    pass


def resetPasswordComplete(request):
    pass