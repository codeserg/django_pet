from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from django.forms import ModelForm
from django.forms.widgets import *
from .models import *
from django import forms
from dal import autocomplete

class VizitForm(ModelForm): 
        
    result_choise=[('Cold', 'Cold'),('Warm', 'Warm'),('Hot', 'Hot')]
    contact_choise= [('0','---')]
    datefact = forms.DateTimeField(widget =DateTimeInput(), label='Дата визита')
    datenext = forms.DateTimeField(required=False, widget =DateTimeInput(), label='Дата следующего визита')
    result= forms.ChoiceField(choices=result_choise,widget=forms.RadioSelect(), label='Результат визита (личная оценка)')
    hint_organization = forms.CharField(label ='Место работы', widget=forms.TextInput(attrs={'style': 'pointer-events: none;'}),required=False)
    hint_special = forms.CharField(label ='Специальность', widget=forms.TextInput(attrs={'style': 'pointer-events: none;'}),required=False)
    
    
    #contact  = forms.CharField(required=False,widget=autocomplete.ModelSelect2(url='Vizit:ContactAuto'))
    class Meta:
        model=Vizit
        fields =  ['kamid','vizstatus','contact','hint_organization','hint_special',"goal",'viztype',"datefact",'result',"datenext",'social_link','nextaction','comment']
        
        widgets = {
            #'contact': autocomplete.ModelSelect2(url='Vizit:ContactAuto'),
            'comment': Textarea(attrs={'cols': 80, 'rows': 3}),
            
            } 


    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(VizitForm, self).__init__(*args, **kwargs)
        kams  = Kam.objects.filter(siteuser=self.request.user)
        if kams:
            kamid = kams[0].pk
            self.fields['contact'].queryset = Contact.objects.filter(kam=kamid, deleted=False ).order_by('name')
        else:
            self.fields['contact'].queryset = Contact.objects.filter(kam=-999)
    

MemberFormset = inlineformset_factory(Event,EventMember, fields = '__all__',extra=5,widgets={'contact': autocomplete.ModelSelect2(url='Vizit:ContactAuto')})

class EventForm(ModelForm): 
        
    inf = '%Y/%m/%d %H:%M'
    print(inf)
    dateevent = forms.DateTimeField(required=False, widget =DateTimeInput(),  label='Дата')

        
    #contact  = forms.CharField(required=False,widget=autocomplete.ModelSelect2(url='Vizit:ContactAuto'))
    class Meta:
        model=Event
        fields = ["dateevent", "goal", "result","kamid","topic"]