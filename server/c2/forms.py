from django.forms import ModelForm
from .models import *

class addCommandForm(ModelForm):
    class Meta:
        model = command
        fields = '__all__'
