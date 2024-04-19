from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Booking,  Service ,Profile, ServiceItem
from django.contrib.auth.models import User, Group


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Retrieve the user from kwargs
        super().__init__(*args, **kwargs)
        self.fields['service_item'].queryset = ServiceItem.objects.filter(owner=user)  # Filter the service items based on the user
    class Meta:
        model = Booking
        fields = ['date','time', 'client_notes', 'service_item']
        labels = {
            'date': 'Date',
            'time': 'Time - round hours only (e.g. 10:00:00, 11:00:00)',
            'client_notes': 'Notes',
            'service_item': 'Service Item',
        }


# class ProfileForm(forms.ModelForm):

#     class Meta:
#         model = Profile
#         fields = ["profile_picture"]


class RegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('client', 'Client'),
        ('service_provider', 'Service Provider'),
    ]

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data.get('user_type')

        if commit:
            user.save()
            # Assign the user to the selected group based on the user_type
            group_name = 'Service Providers' if user_type == 'service_provider' else 'Clients'
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

        return user


class UpdateUsernameForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username']

class UpdatePasswordForm(PasswordChangeForm):
    pass



class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'location', 'contact_details', 'available_spaces', 'image']
        labels = {
            'name': 'Service Name',
            'description': 'Description',
            'location': 'Location',
            'contact_details': 'Contact Details',
            'available_spaces': 'Available Spaces',
            'image': 'Upload a photo',
        }

class ServiceItemForm(forms.ModelForm):
    class Meta:
        model = ServiceItem
        fields = ['identifier','description', 'field_1', 'field_2', 'field_3']
        # Add labels to the fields according to the website you are building
        labels = {
            'identifier': 'License Plate',
            'description': 'Manufacturer',
            'field_1': 'Model',
            'field_2': 'Year of Manufacture',
            'field_3': 'Valid Inspection',
        }
