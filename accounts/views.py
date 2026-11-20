from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FarmerRegistrationForm
from .decorators import role_required
from .models import User


def register(request):

    if request.method == 'POST':
        form = FarmerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = FarmerRegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })


@login_required
def dashboard(request):

    if request.user.role == User.Role.ADMINISTRATOR:
        return redirect('admin_dashboard')

    return redirect('farmer_dashboard')


@role_required(User.Role.FARMER)
def farmer_dashboard(request):
    return render(request, 'accounts/farmer_dashboard.html')


@role_required(User.Role.ADMINISTRATOR)
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')