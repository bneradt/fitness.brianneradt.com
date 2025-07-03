from django.contrib import admin
from .models import WorkoutSession, WorkoutSet

# Register your models here.
admin.site.register(WorkoutSession)
admin.site.register(WorkoutSet)
