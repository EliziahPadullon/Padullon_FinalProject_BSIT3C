from django import forms
from users.models import Users
from users.utils.hash_password import verify_password
from django.conf import settings

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128)
    email = forms.EmailField()
    name = forms.CharField(max_length=150)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Users.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists!")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        domain = email.split('@')[-1]
        if domain not in settings.ALLOWED_EMAIL_DOMAINS:
            raise forms.ValidationError("Email domain not allowed.")
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists!")
        return email

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            raise forms.ValidationError("Username and password are required!")

        user = Users.objects.filter(username=username).first()
        if not user or not verify_password(password, user.password):
            raise forms.ValidationError("Invalid username or password!")

        cleaned_data["user"] = user  # Attach user for use in view
        return cleaned_data
