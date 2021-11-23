from django import forms
from django.forms import ModelForm
from .models import *
from location.models import *

class CountryForm(forms.ModelForm):
    country=forms.ModelChoiceField(queryset=Country.objects.all(),widget=forms.Select(attrs={'class':'country serachselectbox','required':'False'}))
    class Meta:
        model = Country
        fields = '__all__'


class StateForm(forms.ModelForm):
    
    state=forms.ModelChoiceField(queryset=State.objects.all(),widget=forms.Select(attrs={'class':'state serachselectbox','required':'False'}))
    
    class Meta:
        model = State
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country=country_id).order_by('state_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['state'].queryset = self.instance.country.city_set.order_by('state_name')


class CityForm(forms.ModelForm):
    city=forms.ModelChoiceField(queryset=City.objects.all(),widget=forms.Select(attrs={'class':'city serachselectbox','required':'False'}))
    
    class Meta:
        model = City
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                #print(state_id)
                self.fields['city'].queryset = City.objects.filter(state=state_id).order_by('city_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('city_name')



class PincodeForm(forms.ModelForm):
    pincode=forms.ModelChoiceField(queryset=Pincode.objects.all())
    
    class Meta:
        model = Pincode
        fields = '__all__'