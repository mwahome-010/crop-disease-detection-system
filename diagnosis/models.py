
from django.conf import settings
from django.db import models


class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class PlantPart(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Disease(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CropPartDisease(models.Model):
    crop = models.ForeignKey(
        Crop,
        on_delete=models.CASCADE,
        related_name='crop_diseases'
    )

    plant_part = models.ForeignKey(
        PlantPart,
        on_delete=models.CASCADE,
        related_name='part_diseases'
    )

    disease = models.ForeignKey(
        Disease,
        on_delete=models.CASCADE,
        related_name='crop_part_diseases'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['crop', 'plant_part', 'disease'],
                name='unique_crop_part_disease'
            )
        ]

    def __str__(self):
        return (
            f'{self.crop} - {self.plant_part} - {self.disease}'
        )


class Recommendation(models.Model):
    crop_part_disease = models.ForeignKey(
        CropPartDisease,
        on_delete=models.CASCADE,
        related_name='recommendations'
    )

    advice = models.TextField()

    def __str__(self):
        return (
            f'Recommendation for {self.crop_part_disease}'
        )


class Diagnosis(models.Model):

    class Status(models.TextChoices):
        HEALTHY = 'HEALTHY', 'Healthy'
        DISEASE_DETECTED = 'DISEASE_DETECTED', 'Disease detected'
        UNDETERMINED = 'UNDETERMINED', 'Undetermined'

    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='diagnoses'
    )

    crop = models.ForeignKey(
        Crop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    plant_part = models.ForeignKey(
        PlantPart,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    disease = models.ForeignKey(
        Disease,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    image = models.ImageField(upload_to='diagnoses/%Y/%m/')

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.UNDETERMINED
    )

    confidence = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_simulated = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f'{self.farmer.username} - {self.created_at}'
        )
