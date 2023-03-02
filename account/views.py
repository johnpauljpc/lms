from django.shortcuts import render

# Create your views here.
def loginView(request):
    return render(request, 'accounts/login.html')

def registrationView(request):
    return render(request, 'accounts/register.html')