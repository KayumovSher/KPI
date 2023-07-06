from django.contrib import admin
from .models import *
from django import forms
from django.contrib import admin
from .models import KpiModel


class KPIModelForm(forms.ModelForm):
    class Meta:
        models = KpiModel 
        fields = '__all__'

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['league'].widget.attrs['readonly'] = True

    

class KPIAdmin(admin.ModelAdmin):
    form = KPIModelForm
    list_display = ('name', 'book', 'sport', 'work', 'eureka', 'general', 'league', 'koef', 'book_comment')
    

admin.site.register(KpiModel, KPIAdmin)