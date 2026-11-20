
from django.contrib import admin
from .models import (
    Crop,
    PlantPart,
    Disease,
    CropPartDisease,
    Recommendation,
    Diagnosis,
)


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(PlantPart)
class PlantPartAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(CropPartDisease)
class CropPartDiseaseAdmin(admin.ModelAdmin):
    list_display = ('crop', 'plant_part', 'disease')
    list_filter = ('crop', 'plant_part', 'disease')
    search_fields = (
        'crop__name',
        'plant_part__name',
        'disease__name',
    )


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('id', 'crop_part_disease')
    search_fields = (
        'crop_part_disease__crop__name',
        'crop_part_disease__disease__name',
        'advice',
    )


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'farmer',
        'crop',
        'plant_part',
        'disease',
        'status',
        'is_simulated',
        'created_at',
    )
    list_filter = ('status', 'is_simulated', 'created_at')
    search_fields = ('farmer__username', 'crop__name', 'disease__name')
    readonly_fields = ('created_at',)
