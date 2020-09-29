from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        # exclude = ('last_modified',)
        widgets = {'completed_profile': forms.HiddenInput(), 'user': forms.HiddenInput()}
        
        