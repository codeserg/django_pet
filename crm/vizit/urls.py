from django.urls import path,include 
from .views import *
 
app_name = 'Vizit'
urlpatterns = [
    path('', index, name='home'),
     
    path('contactauto/', ContactAutocomplete.as_view(), name='ContactAuto'),
    path("accounts/", include("django.contrib.auth.urls")),  

    path('hintwork/', gethint, name='hintwork'),

    path("visits/", VisitList.as_view(), name='VisitList'),
    path('visit/<pk>/', VizitUpdate.as_view(), name='VisitEdit'),
    path('visit/<pk>/delete/', VizitDelete.as_view(), name='VisitDelete'),
    path("visitadd", VizitCreate.as_view(), name='VisitAdd'),
        
    path('contact/<pk>', ContactUpdate.as_view(), name='ContactEdit'),
    path("contacts/", ContactList.as_view(), name='ContactList'),
    path("contactadd/", ContactCreate.as_view(), name='ContactAdd'),
    path("reports/kpi", ReportKpi, name='ReportKpi'),
    path("reports/cont", export_excel_vrach, name='ReportContact'),
    
    path("exp", export_excel, name='export_excel'),
    path("activity", ShowActivity.as_view(), name='show_activity'),
    path("exp_kpi", export_excel_kpi, name='export_excel_kpi'),
    path("exp_event", export_excel_events, name='export_excel_events'),
    path("exp_event_short", export_excel_events_short, name='export_excel_events'),

    path("initfreq", initinsert, name='initinsert'),
    
    #path("destroy", deletecontactlist, name='delcontactlist'),
    
    path("events", EventList.as_view(), name='EventList'),
    path('eventadd', EventCreateView.as_view(), name='EventCreate'),
    path('event/<pk>', EventUpdateView.as_view(), name='EventUpdate'),
    
    path('test', TestView.as_view(), name='EventUpdate'),
]