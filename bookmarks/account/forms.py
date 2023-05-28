from django import forms
from .models import Profile


# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        # Commit = True -> Store data to tha database right now.
        # Commit = False -> Store data temporary not to tha database right now.
        user = super().save(commit)
        # Password security
        user.set_password(self.cleaned_data['password'])
        # Save a new user object
        user.save()
        return user

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    # to check if the email is using by other users
    def clean_email(self):
        data = self.cleaned_data['email']
        if Profile.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'photo']

    # to check if the email is using by other users
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = Profile.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError(' Email already in use.')
        return data
