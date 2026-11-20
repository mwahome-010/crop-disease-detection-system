GUEST_DIAGNOSIS_LIMIT = 3


def get_guest_diagnoses_used(request):
    return request.session.get('guest_diagnoses_used', 0)


def guest_limit_reached(request):
    return (
        get_guest_diagnoses_used(request)
        >= GUEST_DIAGNOSIS_LIMIT
    )


def increment_guest_diagnoses(request):
    current_count = get_guest_diagnoses_used(request)

    request.session['guest_diagnoses_used'] = current_count + 1
    request.session.modified = True