from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Hobby

class CustomUserCreationForm(UserCreationForm):
    date_of_birth: forms.DateField = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    hobbies: forms.CharField = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Enter hobbies separated by commas'})
    )

    class Meta(UserCreationForm.Meta):
        model: type = CustomUser
        fields: tuple[str, ...] = ('username', 'email', 'date_of_birth')  

    def save(self, commit: bool = True) -> CustomUser:
        user: CustomUser = super().save(commit=False)
        if commit:
            user.save()

        hobbies_text: str = self.cleaned_data.get('hobbies', '')
        if hobbies_text:
            hobby_names = [h.strip() for h in hobbies_text.split(',') if h.strip()]
            for name in hobby_names:
                hobby, _ = Hobby.objects.get_or_create(name=name)
                user.hobbies.add(hobby)

        if commit:
            self.save_m2m()

        return user

class CustomUserChangeForm(UserChangeForm):
    date_of_birth: forms.DateField = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    hobbies: forms.ModelMultipleChoiceField = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    new_hobby: forms.CharField = forms.CharField(
        required=False,
        help_text="Add a new hobby if not listed"
    )

    class Meta:
        model: type = CustomUser
        fields: tuple[str, ...] = ('username', 'email', 'date_of_birth', 'hobbies', 'new_hobby')

    def save(self, commit: bool = True) -> CustomUser:
        user: CustomUser = super().save(commit=False)

        if commit:
            user.save()

            
        if commit:
            self.save_m2m()

        new_hobby_name: str = self.cleaned_data.get('new_hobby', '')
        if new_hobby_name:
            hobby, _ = Hobby.objects.get_or_create(name=new_hobby_name)
            user.hobbies.add(hobby)

        return user
