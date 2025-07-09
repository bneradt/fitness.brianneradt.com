from django import forms
from .models import WorkoutSession

class WorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = [
            'date',
            'pullup_type',
            'pullup_count1',
            'pushup_count1',
            'pullup_count2',
            'pushup_count2',
            'pullup_count3',
            'pushup_count3'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Default the date field to today if not provided
        if not self.instance.pk and not self.data.get('date'):
            from django.utils import timezone
            # Use localdate to respect TIME_ZONE and avoid UTC shift
            self.fields['date'].initial = timezone.localdate()
