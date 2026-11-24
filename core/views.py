from django.shortcuts import render
from diagnosis.forms import ImageUploadForm
from diagnosis.guest_limits import (
    GUEST_DIAGNOSIS_LIMIT, get_guest_diagnoses_used, guest_limit_reached)

def home(request):
    context = {'form': ImageUploadForm()}
    if not request.user.is_authenticated:
        used = get_guest_diagnoses_used(request)
        context.update(
            guest_limit=GUEST_DIAGNOSIS_LIMIT,
            guest_remaining=max(GUEST_DIAGNOSIS_LIMIT - used, 0),
            guest_limit_reached=guest_limit_reached(request),
        )
    return render(request, 'core/home.html', context)