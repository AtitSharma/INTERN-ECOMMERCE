from django import forms
from django.conf import settings
from useraccount.models import User


class UserRegisterForm(forms.Form):
    username=forms.CharField(max_length=255)
    password1=forms.CharField(max_length=255,widget=forms.PasswordInput)
    password2=forms.CharField(max_length=255,widget=forms.PasswordInput)
    email=forms.EmailField()
    
    def clean_username(self):
        username=self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User already exits")
        return username
    
    
    def clean_password2(self):
        password1=self.cleaned_data.get("password1")
        password2=self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Enter same password")
            elif len(password2)<5:
                raise forms.ValidationError("Password must be atleast 5 characters")
            return password2    
            
        raise forms.ValidationError("Enter Password on both fields")
    
    def clean_email(self):
        email=self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exits !!")
        return email
        
    def save(self):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password2")
        email=self.cleaned_data.get("email")
        user=User.objects.create_user(username=username,password=password,email=email)         
        return user


class UserLoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(max_length=255,widget=forms.PasswordInput)
    