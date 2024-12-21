# from django import forms
# from .models import CustomUser
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import UserChangeForm

# class CustomUserCreationForm(UserCreationForm):
#     date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     hobbies = forms.CharField(required=False, widget=forms.Textarea())

#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ('username', 'email', 'date_of_birth', 'hobbies')


# class CustomUserChangeForm(UserChangeForm):
#     password = None  # We remove the password field here, separate form for that
#     date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     hobbies = forms.CharField(required=False, widget=forms.Textarea())

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'date_of_birth', 'hobbies')


from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Hobby

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    # Let users type their hobbies as comma-separated text.
    hobbies = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Enter hobbies separated by commas'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Do NOT include 'hobbies' here, since it's a M2M field and we are overriding it as CharField
        fields = ('username', 'email', 'date_of_birth')  

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        # Now handle hobbies separately
        hobbies_text = self.cleaned_data.get('hobbies', '')
        if hobbies_text:
            hobby_names = [h.strip() for h in hobbies_text.split(',') if h.strip()]
            for name in hobby_names:
                hobby, created = Hobby.objects.get_or_create(name=name)
                user.hobbies.add(hobby)

        # Now save the M2M relationships
        if commit:
            self.save_m2m()

        return user

class CustomUserChangeForm(UserChangeForm):
    password = None
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    new_hobby = forms.CharField(
        required=False,
        help_text="Add a new hobby if not listed"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth', 'hobbies', 'new_hobby')

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

    # First, save the selected hobbies from the form
        if commit:
            self.save_m2m()

        # Now, handle the new hobby after the user's chosen hobbies are set
        new_hobby_name = self.cleaned_data.get('new_hobby')
        if new_hobby_name:
            hobby, created = Hobby.objects.get_or_create(name=new_hobby_name)
            user.hobbies.add(hobby)

        return user
