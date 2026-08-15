from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotAllowed
from django.utils.http import url_has_allowed_host_and_scheme
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
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()

        # check if username exists
        if User.objects.filter(username=username).exists():
            messages.warning(request, f"the username <b>{username}</b> already exists!")
            return redirect('register')
        # check if email already exists
        if User.objects.filter(email=email).exists():
            messages.warning(request, f'the email: <b>{email}</b> has been taken already!')
            return redirect('register')

        if password1 != password2:
            messages.info(request, 'password does not match')
            return redirect('register')

        try:
            validate_password(password1)
        except ValidationError as errors:
            for error in errors:
                messages.error(request, error)
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, f'welcome <b>{user.username}</b>! You can now login')
        return redirect('login')

    return render(request, 'accounts/register.html')


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # redirecting to the previous page if any
            next_url = request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
            ):
                return redirect(next_url)
            messages.info(request, f"welcome {user}")
            return redirect('home')
        else:
            messages.error(request, 'Invalid username, email or password')
            return redirect('login')

    if request.user.is_authenticated:
        return redirect('home')

    if request.GET.get('next'):
        messages.info(request, 'To continue, please <b>login</b>!')

    return render(request, 'accounts/login.html')


def logoutView(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    logout(request)
    messages.info(request, 'You have logged out')
    return redirect('home')


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
                    return redirect('reset-password-done')
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")
            messages.warning(request, f"{user_email} is not associated to any registered User")
            return redirect('reset-password')

        for error in form.errors.as_data().values():
            messages.error(request, error[0].messages[0])
                
        
                



    form = passwordResetForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/password_reset_form.html', context)


def passwordResetConfirmation(request, uidb64, token):

    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = changePasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = changePasswordForm(user)
        context = {
            'form':form
        }
        return render(request, 'accounts/password_reset_confirm.html', context)
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('reset-password')


def resetPasswordDone(request):
    return render(request, "accounts/password_reset_done.html")


@login_required(login_url='login')
def profile(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password', '')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name

        if password:
            try:
                validate_password(password, user=user)
            except ValidationError as errors:
                for error in errors:
                    messages.error(request, error)
                return redirect('profile')
            user.set_password(password)

        user.save()
        if password:
            update_session_auth_hash(request, user)
        messages.success(request, 'Profile successfully updated.')
        return redirect('profile')
    return render(request, "accounts/profile.html")