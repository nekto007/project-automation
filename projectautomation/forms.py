from django import forms

from .models import TimeSlot


class ChooseTimeForm(forms.Form):
    best_time_slots = forms.ModelMultipleChoiceField(
        label='Наиболее удобное время (*время московское)',
        queryset=TimeSlot.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
