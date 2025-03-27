from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms import ModelForm

class LoginForm(AuthenticationForm):
    username = UsernameField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

class UserForm(forms.ModelForm):
    # Custom password fields
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }



class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = [ 'contact', 'address', 'userpic']  # Specify the fields to display in the form
        widgets = {
              # User select dropdown
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Information'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            
        }


from .models import Volunteer

class VolunteerForm(forms.ModelForm):

    class Meta:
        model = Volunteer
        fields = [ 'contact',  'userpic', 'idpic', 'aboutme', 'address' ]
        
        # Customizing widgets for Bootstrap styling
        widgets = {
           
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'aboutme': forms.Textarea(attrs={'class': 'form-control'}),
            'userpic': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'idpic': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }




from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate

from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label="Confirm New Password"
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        user = self.user

        # Authenticate the user with the provided old password
        if not user.check_password(old_password):
            raise forms.ValidationError("The old password is incorrect.")
        return old_password
    

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donationname', 'donationpic', 'collectionloc', 'description']  # Only four fields

    # Applying Bootstrap classes to form fields
    donationname = forms.ChoiceField(
        choices=Donation.DONATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    donationpic = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    collectionloc = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Collection Location'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Description', 'rows': 4})
    )

class DonationAreaForm(forms.ModelForm):
    class Meta:
        model = DonationArea
        fields = ['arename', 'description']

    # Add custom __init__ method to add Bootstrap class to each field
    def __init__(self, *args, **kwargs):
        super(DonationAreaForm, self).__init__(*args, **kwargs)
        # Adding Bootstrap classes to form fields
        self.fields['arename'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})