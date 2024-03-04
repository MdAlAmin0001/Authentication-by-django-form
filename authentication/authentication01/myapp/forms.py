from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Custom_user




class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Enter Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    user_type = forms.ChoiceField(label='User Type', choices=Custom_user.USER, widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Custom_user
        fields = ['first_name', 'last_name', 'username', 'display_name', 'email','user_type','password1','password2']

class login_form(forms.Form):
    username = forms.CharField(label="Enter Username", widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Enter Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Custom_user
        fields = ['first_name', 'last_name', 'display_name', 'profile_pic', 'age', 'gender', 'phone', 'Present_address', 'permanent_address']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'display_name': 'Display Name',
            'profile_pic': 'Profile Picture',
            'age': 'Age',
            'gender': 'Gender',
            'phone': 'Phone',
            'Present_address': 'Present Address',
            'permanent_address': 'Permanent Address',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'Present_address': forms.TextInput(attrs={'class': 'form-control'}),
            'permanent_address': forms.TextInput(attrs={'class': 'form-control'}),
        }