from django.contrib import admin
from .models import Kam, Contact,Vizit, VizitFreq,Event,EventMember,EventTopic

class ContactAdmin (admin.ModelAdmin):
    list_display = ('name','spec','category', 'kam')
    list_display_links = ('name',)
    search_fields = ('name',)
    radio_fields = {'spec':admin.VERTICAL, 'category_account':admin.VERTICAL}
    autocomplete_fields = ('kam',)

class KamAdmin (admin.ModelAdmin):
    search_fields = ('name',)

class VizitAdmin(admin.ModelAdmin):
    autocomplete_fields = ('contact',)
    list_display = ('kamid','viztype','contact', 'datefact')
    #list_display_links = ('organization',)

class VizitFreqAdmin(admin.ModelAdmin):
    list_display = ('kamid','year','month','workdays','dayoff_minus', 'dayadm_minus','workday_count','contact_count_a','contact_count_b','contact_count_c',
    'plan_count_a','plan_count_b','plan_count_c','freq_a','freq_b','freq_c' )

# Register your models here.

admin.site.register(Kam, KamAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Vizit,VizitAdmin)
admin.site.register(VizitFreq,VizitFreqAdmin)
admin.site.register(Event)
admin.site.register(EventMember)
admin.site.register(EventTopic)
