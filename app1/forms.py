from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model
from .models import User,BillingAddress, ShippingAddress


User = get_user_model()

class SimpleSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username or Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control-file'})
        self.fields.pop('password')  # Remove password field from the form



class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'street_address', 'apartment_address',
                  'city', 'state', 'zip_code', 'country']
        widgets = {
            'apartment_address': forms.TextInput(attrs={'required': False}),
        }


class ShippingAddressForm(forms.ModelForm):
    same_as_billing = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'phone',
                  'street_address', 'apartment_address',
                  'city', 'state', 'zip_code', 'country', 'notes']
        widgets = {
            'apartment_address': forms.TextInput(attrs={'required': False}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'same_as_billing':
                self.fields[field].required = False


class EmailForm(forms.Form):
    receiver = forms.EmailField(label='Receiver Email')
    subject = forms.CharField(label='Subject', max_length=100)
    body = forms.CharField(label='Message', widget=forms.Textarea)