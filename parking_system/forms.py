from django import forms
from .models import Vehicle, SignOut
import re # This is a tool for "Pattern Matching" (Regex)

class VehicleRegistrationForm(forms.ModelForm):
    driver_name = forms.CharField(
        error_messages={'required': 'Please enter the driver\'s full name.'}
    )
    number_plate = forms.CharField(
        error_messages={'required': 'The vehicle number plate is required for security.'}
    )
    phone_number = forms.CharField(
        error_messages={'required': 'A phone number is needed to contact the owner.'}
    )
    class Meta:
        model = Vehicle
        fields = [
            'driver_name', 'vehicle_type', 'number_plate', 
            'vehicle_model', 'vehicle_color', 'phone_number', 'nin_number'
        ]

    def clean_driver_name(self):
        name = self.cleaned_data.get('driver_name')
        if not name[0].isupper(): # This ensures that the first character in position 0 is a capital letter
            raise forms.ValidationError("The name must start with a capital letter.")
        if any(char.isdigit() for char in name): # This ensures that all characters put in are letters and so numbers are rejected
            raise forms.ValidationError("The name cannot contain numbers.")
        return name

    def clean_number_plate(self):
        plate = self.cleaned_data.get('number_plate')
        if not plate.startswith('U'): # This ensures that the number plates put in all start with'U'
            raise forms.ValidationError("Number plate must start with 'U'.")
        if len(plate) > 6: # This ensures that the number plates put in are not more than 6 characters
            raise forms.ValidationError("Number plate must be less than 6 characters.")
        if not plate.isalnum(): # This ensures that the number plates put in are alphanumeric (letters and numbers only)
            raise forms.ValidationError("Number plate must be alphanumeric (letters and numbers only).")
        return plate
 
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        # Simple check for Ugandan format (e.g., starts with 07 or +256)
        if not re.match(r'^(?:\+256|0)7[0-9]{8}$', phone):
            raise forms.ValidationError("Please enter a valid Ugandan phone number.")
        return phone
    
    def clean(self):
        # This 'clean' method checks the WHOLE form at once
        cleaned_data = super().clean()
        vehicle_type = cleaned_data.get("vehicle_type")
        nin_number = cleaned_data.get("nin_number")

        # Logic: If it's a Boda-boda, the NIN must not be empty
        if vehicle_type == 'BODA' and not nin_number:
            self.add_error('nin_number', "NIN Number is mandatory for Boda-boda riders.")
            
        return cleaned_data
    
    from .models import SignOut

class SignOutForm(forms.ModelForm):
    class Meta:
        model = SignOut
        fields = ['receiver_name', 'phone_number', 'gender', 'nin_number']

    def clean_receiver_name(self):
        name = self.cleaned_data.get('receiver_name')
        if not name[0].isupper():
            raise forms.ValidationError("Receiver name must start with a capital letter.")
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Names cannot contain numbers.")
        return name