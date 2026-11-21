from django.shortcuts import render
from django.core.exceptions import ValidationError

from .forms import ImageUploadForm
from .image_processing import preprocess_image
from .prediction import simulate_prediction
from .guest_limits import (
    guest_limit_reached,
    get_guest_diagnoses_used,
    increment_guest_diagnoses
)

from django.core.files.base import ContentFile
from .models import Crop, PlantPart, Disease, Diagnosis, CropPartDisease
from django.contrib.auth.decorators import login_required

def upload_image(request):

    if (
        not request.user.is_authenticated
        and guest_limit_reached(request)
    ):
        return render(
            request,
            'diagnosis/upload.html',
            {
                'form': ImageUploadForm(),
                'guest_limit_reached': True,
                'guest_diagnoses_used': get_guest_diagnoses_used(request)
            }
        )

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.cleaned_data['image']

            try:
                processed_image = preprocess_image(image)

                prediction = simulate_prediction()

                # Retrieve the matching crop, plant part and disease
                crop = Crop.objects.get(name=prediction['crop'])
                plant_part = PlantPart.objects.get(name=prediction['plant_part'])
                disease = Disease.objects.get(name=prediction['disease'])

                # Confirm that this is a valid combination
                crop_part_disease = CropPartDisease.objects.get(
                    crop=crop,
                    plant_part=plant_part,
                    disease=disease
                )

                # Retrieve the recommendation from the database
                recommendation = crop_part_disease.recommendations.first()

                if recommendation:
                    prediction['recommendation'] = recommendation.advice
                else:
                    prediction['recommendation'] = (
                        'No recommendation is currently available for this diagnosis.'
                    )

                # Save diagnosis only for registered users
                if request.user.is_authenticated:
                    diagnosis = Diagnosis(
                        farmer=request.user,
                        crop=crop,
                        plant_part=plant_part,
                        disease=disease,
                        status=Diagnosis.Status.DISEASE_DETECTED,
                        confidence=None,
                        is_simulated=True
                    )

                    diagnosis.image.save(
                        image.name.rsplit('.', 1)[0] + '.jpg',
                        ContentFile(processed_image.getvalue()),
                        save=False
                    )

                    diagnosis.save()

                else:
                    increment_guest_diagnoses(request)

                return render(
                    request,
                    'diagnosis/diagnosis_result.html',
                    {
                        'image_name': image.name,
                        'prediction': prediction
                    }
                )

            except (
                ValidationError,
                Crop.DoesNotExist,
                PlantPart.DoesNotExist,
                Disease.DoesNotExist,
                CropPartDisease.DoesNotExist
            ) as error:
                form.add_error('image', str(error))

    else:
        form = ImageUploadForm()

    context = {'form': form}

    if not request.user.is_authenticated:
        context['guest_diagnoses_used'] = (
            get_guest_diagnoses_used(request)
        )

    return render(request, 'diagnosis/upload.html', context)

@login_required
def diagnosis_history(request):
    diagnoses = Diagnosis.objects.filter(
        farmer=request.user
    ).order_by('-created_at')

    return render(
        request,
        'diagnosis/diagnosis_history.html',
        {'diagnoses': diagnoses}
    )