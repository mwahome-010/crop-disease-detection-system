from django.shortcuts import render


def home(request):

    context = {}

    if not request.user.is_authenticated:
        guest_count = request.session.get(
            'guest_diagnoses_used', 0
        )

        context['guest_diagnoses_used'] = guest_count

    return render(request, 'core/home.html', context)