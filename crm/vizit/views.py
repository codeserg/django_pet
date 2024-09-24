import io
import locale
from unicodedata import category
#from http.client import HTTPResponse
from django.shortcuts import render, HttpResponseRedirect
from .models import EventMember, Vizit, Contact, Kam,VizitFreq, Event,EventTopic
from django.views.generic.edit import UpdateView, CreateView,DeleteView
from django.urls import reverse
from .forms import VizitForm,  MemberFormset, EventForm
from django.db import connection
from dal import autocomplete
from django.http import HttpResponse,JsonResponse, Http404
from django.views.generic.list import ListView
import csv 
from xlsxwriter.workbook import Workbook
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from dateutil.relativedelta import relativedelta

from django.forms.widgets import *
# Create your views here.

def export_excel_vrach(request):

    if request.user.is_authenticated == False :
        return HttpResponseRedirect("/accounts/login")
    
    output = io.BytesIO()

    workbook = Workbook(output, {'in_memory': True,'remove_timezone': True})
    worksheet = workbook.add_worksheet()
    date_format = workbook.add_format({'num_format': 'dd.mm.yy'})

    if str(request.user) =='coder' or str(request.user)=='pet':
            vrach= Contact.objects.filter(deleted=False)
    else:
            us = Kam.objects.filter(siteuser= request.user )
            vrach= Contact.objects.filter(deleted=False,kam=us[0].pk)

    maxrow = vrach.count()+2

    worksheet.add_table(2,0,maxrow,15,{'columns': [{'header': 'Кам'},
                                          {'header': 'фио'},
                                          {'header': 'Специальность'},
                                          {'header': 'Телефон'},
                                          {'header': 'Email'},
                                          
                                          {'header': 'Fillers Category Potencial'},
                                          {'header': 'Fillers Loyalty'},
                                          {'header': 'Biostimulators Category Potential'},
                                          {'header': 'Biostimulators Loyalty'},
                                          {'header': 'IDP Category'},
                                          {'header': 'IDP Loyalty'},

                                          {'header': 'Город'},
                                          {'header': 'Место работы'},
                                          {'header': 'Комментарий'},
                                          {'header': 'Наименование в DB'},
                                          {'header': 'Дата создания'},  
                                          ]})

    row=3

    for v in vrach:

        worksheet.write(row, 0, str(v.kam))
        worksheet.write(row, 1, v.name)
        
        worksheet.write(row, 2, v.spec)
        worksheet.write(row, 3, v.phone)
        worksheet.write(row, 4, v.email)
        worksheet.write(row, 5, v.cat_filler_potencial)
        worksheet.write(row, 6, v.cat_filler_loyalty)
        worksheet.write(row, 7, v.cat_biostim_potencial)
        worksheet.write(row, 8, v.cat_biostim_loyalty)
        worksheet.write(row, 9, v.cat_idp_potencial)
        worksheet.write(row, 10, v.cat_idp_loyalty)

        worksheet.write(row, 11, v.city)
        worksheet.write(row, 12, v.work_place)
        worksheet.write(row, 13, v.comment)
        worksheet.write(row, 14, v.name_dashboard)
        worksheet.write_datetime(row, 15, v.date_create,date_format)
        
     
        
        row+=1

    worksheet.write(0, 0, 'Список контактов')
    #worksheet.write(0, 2,str(request.user))
    workbook.close()

    output.seek(0)
    today = datetime.datetime.today()
    outfilename = today.strftime('Contacts %d %B %Y %H %M.xlsx')

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=" + outfilename

    output.close()

    return response


def export_excel_events(request):

    if request.user.is_authenticated == False :
        return HttpResponseRedirect("/accounts/login")
    
    output = io.BytesIO()

    workbook = Workbook(output, {'in_memory': True,'remove_timezone': True})
    worksheet = workbook.add_worksheet()
    date_format = workbook.add_format({'num_format': 'dd.mm.yy'})

    eventlist= Event.objects.all()
    
    
    row=2

    for v in eventlist:

        #topic_name = EventTopic.objects.get(id = v.topic)

        doc = Kam.objects.get(pk=v.kamid.pk)
        
        #worksheet.write(row, 0, str(v.kamid))
        worksheet.write(row, 0, doc.name)
        worksheet.write(row, 1, str(v.topic))
        worksheet.write_datetime(row, 2, v.dateevent,date_format)
        worksheet.write(row, 3, v.city)
 
        members = EventMember.objects.filter(parentevent = v.id)

        for m in members:
            row+=1
            worksheet.write(row, 4, str(m.contact))   

        
        
        
        row+=1

    worksheet.write(0, 0, 'Список мероприятий')
    

    worksheet.set_column('A:A', 30)  
    worksheet.set_column('B:B', 80)  
    worksheet.set_column('C:C', 20) 
    worksheet.set_column('D:D', 30)

    workbook.close()

    output.seek(0)
    today = datetime.datetime.today()
    outfilename = today.strftime('events %d %B %Y %H %M.xlsx')

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=" + outfilename

    output.close()

    return response

def export_excel_events_short(request):

    if request.user.is_authenticated == False :
        return HttpResponseRedirect("/accounts/login")
    
    output = io.BytesIO()

    workbook = Workbook(output, {'in_memory': True,'remove_timezone': True})
    worksheet = workbook.add_worksheet()
    date_format = workbook.add_format({'num_format': 'dd.mm.yy'})

    eventlist= Event.objects.all()
    
    
    row=2
   
    for v in eventlist:

        #topic_name = EventTopic.objects.get(id = v.topic)
        
        doc = Kam.objects.get(pk=v.kamid.pk)
        
        #worksheet.write(row, 0, str(v.kamid))
        worksheet.write(row, 0, doc.name)
        worksheet.write(row, 1, str(v.topic))
        worksheet.write_datetime(row, 2, v.dateevent,date_format)
        worksheet.write(row, 3, v.city)
        
        members = EventMember.objects.filter(parentevent = v.id)
        worksheet.write(row, 4, len(members))    
        mmbs =''
        for m in members:
            mmbs += str(m.contact) +'\n'

        worksheet.write_comment(row,4, mmbs,{'width': 200,'height': 300})
        
        
        row+=1

    worksheet.write(0, 0, 'Список мероприятий')
    

    worksheet.set_column('A:A', 30)  
    worksheet.set_column('B:B', 80)  
    worksheet.set_column('C:C', 20) 
    worksheet.set_column('D:D', 30)

    workbook.close()

    output.seek(0)
    today = datetime.datetime.today()
    outfilename = today.strftime('events %d %B %Y %H %M.xlsx')

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=" + outfilename

    output.close()

    return response


def export_excel(request):

    if request.user.is_authenticated == False :
        return HttpResponseRedirect("/accounts/login")
    
    output = io.BytesIO()

    workbook = Workbook(output, {'in_memory': True,'remove_timezone': True})
    worksheet = workbook.add_worksheet()
    date_format = workbook.add_format({'num_format': 'dd.mm.yy'})

    if str(request.user) =='coder' or str(request.user)=='pet':
            vizits= Vizit.objects.all()
    else:
            us = Kam.objects.filter(siteuser= request.user )
            vizits= Vizit.objects.filter(kamid=us[0].pk)

    maxrow = vizits.count()+2

    worksheet.add_table(2,0,maxrow,13,{'columns': [{'header': 'Кам'},
                                          {'header': 'Тип визита'},
                                          {'header': 'Дата визита'},
                                          {'header': 'Дата след.'},
                                          {'header': 'Дата создания'},
                                          {'header': 'Цель'},
                                          {'header': 'Дальн. действия'},
                                          {'header': 'Соц. сети'},
                                          {'header': 'Результат'},
                                          {'header': 'Комментарий'},
                                          {'header': 'Организация'},
                                          {'header': 'Специальность'},
                                          {'header': 'Статус'}, 
                                          {'header': 'ФИО врача'},  
                                          ]})

    row=3

    for v in vizits:


        #fio = Contact.objects.get(kamid=us[0].pk)

        worksheet.write(row, 0, str(v.kamid))
        worksheet.write(row, 1, v.viztype)
        
        worksheet.write_datetime(row, 2, v.datefact,date_format)
        worksheet.write(row, 3, v.datenext,date_format)
        worksheet.write(row, 4, v.datecreate,date_format)
        worksheet.write(row, 5, v.goal)
        worksheet.write(row, 6, v.nextaction)
        worksheet.write(row, 7, v.social_link)
        worksheet.write(row, 8, v.result)
        worksheet.write(row, 9, v.comment)
        worksheet.write(row, 10, v.hint_organization)
        worksheet.write(row, 11, v.hint_special)
        worksheet.write(row, 12, v.vizstatus)
        worksheet.write(row, 13, str(v.contact))

        
        
        row+=1

    worksheet.write(0, 0, 'Визитная активность')
    #worksheet.write(0, 2,str(request.user))
    workbook.close()

    output.seek(0)
    today = datetime.datetime.today()
    outfilename = today.strftime('Visits %d %B %Y %H %M.xlsx')

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=" + outfilename

    output.close()

    return response


def export_excel_kpi(request):
    if request.user.is_authenticated == False :
        return HttpResponseRedirect("/accounts/login")
    output = io.BytesIO()

    workbook = Workbook(output, {'in_memory': True,'remove_timezone': True})
    worksheet = workbook.add_worksheet()
    date_format = workbook.add_format({'num_format': 'dd.mm.yy'})

    vizits= VizitFreq.objects.all()
    maxrow = vizits.count()+2

    worksheet.add_table(2,0,maxrow,21,{'columns': [
                                          {'header': 'Кам'},
                                          {'header': 'Месяц'},
                                          {'header': 'Дней в мес'},
                                          {'header': 'Выходные'},
                                          {'header': 'Адм. работа'},
                                          {'header': 'Дней работы'},

                                          {'header': 'Всего врачей А'},
                                          {'header': 'План визитов А'},
                                          {'header': 'План частоты А'},
                                          {'header': 'Визитов сделано А'},
                                          {'header': 'Выполнение % А'},
                                          
                                          {'header': 'Всего врачей B'},
                                          {'header': 'План визитов B'},
                                          {'header': 'План частоты B'},
                                          {'header': 'Визитов сделано B'},
                                          {'header': 'Выполнение % B'},
                                          
                                          {'header': 'Всего врачей C'},
                                          {'header': 'План визитов C'},
                                          {'header': 'План частоты C'},
                                          {'header': 'Визитов сделано C'},
                                          {'header': 'Выполнение % C'},
                                          
                                          {'header': 'Суммарная частота'}
                                          ]})

    row=3

    for v in vizits:

        worksheet.write(row, 0, str(v.kamid))
        worksheet.write(row, 1, v.month)
        worksheet.write(row, 2, v.workdays)
        worksheet.write(row, 3, v.dayoff_minus)
        worksheet.write(row, 4, v.dayadm_minus)
        worksheet.write(row, 5, v.workday_count)

        worksheet.write(row, 6, v.contact_count_a)
        worksheet.write(row, 7, v.plan_count_a)
        worksheet.write(row, 8, v.freq_a)
        worksheet.write(row, 9, v.fact_count_a)
        worksheet.write(row, 10, v.procent_a)

        worksheet.write(row, 11, v.contact_count_b)
        worksheet.write(row, 12, v.plan_count_b)
        worksheet.write(row, 13, v.freq_b)
        worksheet.write(row, 14, v.fact_count_b)
        worksheet.write(row, 15, v.procent_b)

        worksheet.write(row, 16, v.contact_count_c)
        worksheet.write(row, 17, v.plan_count_c)
        worksheet.write(row, 18, v.freq_c)
        worksheet.write(row, 19, v.fact_count_c)
        worksheet.write(row, 20, v.procent_c)
        
        worksheet.write(row, 21, v.freq_total)

        
        
        row+=1

    worksheet.write(0, 0, 'KPI по визитной активности')
    
    workbook.close()

    output.seek(0)
    today = datetime.datetime.today()
    outfilename = today.strftime('KPI Visits %d %B %Y %H %M.xlsx')

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=" + outfilename

    output.close()

    return response

def export_csv(request):
    books = Vizit.objects.all()
    response = HttpResponse(books , content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="books.xls"'

    writer = csv.writer(response)
    writer.writerow(['Book', 'Author'])
    for book in books:
        writer.writerow([book.viztype, book.datefact])

    return response

class ShowActivity (LoginRequiredMixin, ListView):
    context_object_name = 'Vizit'
    model = Vizit
    template_name= 'vizit/vizit_activity.html'

    def get_queryset(self):
        datebegin = datetime.date(2023,1,11)
        dateend = datetime.date(2023,1,12)
        ret= Vizit.objects.order_by('-datecreate')[:5]
        return ret
        

class VisitList (LoginRequiredMixin, ListView):
    context_object_name = 'Vizit'
    model = Vizit
    paginate_by = 30

    def get_queryset(self):
        queryset = super(VisitList, self).get_queryset()
                
        if self.request.GET.get('category_account'):
            onlycont = Contact.objects.filter (category_account=self.request.GET.get('category_account'))
            queryset= queryset.filter(contact__in=onlycont)
        
        if self.request.GET.get('vizit_status'):
            queryset= queryset.filter(vizstatus=self.request.GET.get('vizit_status'))
        
        if self.request.GET.get('kamid'):
            queryset= queryset.filter(kamid=self.request.GET.get('kamid'))

        usr = str(self.request.user)

        if usr !='coder' and usr!='pet':
            us = Kam.objects.filter(siteuser= self.request.user )
            queryset= queryset.filter(kamid=us[0].pk)
            
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super(VisitList, self).get_context_data(**kwargs)
        
        km =Kam.objects.filter(siteuser= self.request.user )
        if km:
            cdt = datetime.datetime.now()
            freq = VizitFreq.objects.filter (month =cdt.month, year = cdt.year, kamid =km[0])
            ctx['rate'] = freq.values()[0]
            ctx['ratetitle'] = gettitle(self.request)
        return ctx
    
    
class ContactList (LoginRequiredMixin,ListView):
    context_object_name = 'Contact'
    model = Contact
    paginate_by = 30
    
    def get_queryset(self):
        queryset = super(ContactList, self).get_queryset()
                
        if self.request.GET.get('category_account'):
            queryset= queryset.filter(category_account=self.request.GET.get('category_account'))

        if self.request.GET.get('kamid'):
            queryset= queryset.filter(kam=self.request.GET.get('kamid'))
        
        if self.request.GET.get('fio'):
            queryset= queryset.filter(name__icontains=self.request.GET.get('fio'))
       
        return queryset

def index(request):
    if request.user.is_authenticated == False :
        return HttpResponseRedirect("/accounts/login")
    
    context= {'user':request.user}
    return render(request,'vizit/home.html', context)

def gettitle(req):
    km =Kam.objects.filter(siteuser= req.user)
    kmname=km[0].name if km else ''
    cdt = datetime.datetime.now()
    
    return {"MonthName":datetime.datetime.now().strftime("%B"),
            "YearName":datetime.datetime.now().strftime("%Y"),
            "KamName":kmname}

def ReportKpi(request):
    if request.user.is_authenticated == False :
        return HttpResponseRedirect("/accounts/login")
    
    viz= VizitFreq.objects.none
    context= dict()
    km =Kam.objects.filter(siteuser= request.user )
    if km:
        cdt = datetime.datetime.now()
        freq = VizitFreq.objects.filter (month =cdt.month, year = cdt.year, kamid =km[0])
        context['rate'] = freq.values()[0]
        context['ratetitle'] = gettitle(request)

    if request.GET.get('month'):
        calculon(int(request.GET.get('year')),int(request.GET.get('month')))
        
        viz= VizitFreq.objects.filter(month=request.GET.get('month'),year=request.GET.get('year'))
        viz= viz.order_by('kamname')
        context ['report']=viz
        context ['month']=request.GET.get('month')
        context ['year']=request.GET.get('year')
    return render(request,'vizit/vizit_kpi.html', context)

class ContactUpdate (LoginRequiredMixin, UpdateView):
    model = Contact
    fields= ['name','spec','phone','email','city','kam','cat_filler_potencial','cat_filler_loyalty','cat_biostim_potencial','cat_biostim_loyalty','cat_idp_potencial','cat_idp_loyalty','work_place','comment','name_dashboard']

    def get_success_url(self):
        return reverse("Vizit:ContactList")

class VizitUpdate (LoginRequiredMixin,UpdateView):
    model = Vizit
    form_class = VizitForm
        
    def get_success_url(self):
        return reverse("Vizit:home")

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(VizitUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        
        return kwargs
    
    def get_context_data(self, **kwargs):
        ctx = super(VizitUpdate, self).get_context_data(**kwargs)
        ctx['updatemode'] = 'update'
        return ctx
    
    def get_initial(self):
        self.initial={}
        
        return super(VizitUpdate, self).get_initial()

class VizitCreate (LoginRequiredMixin,CreateView):
    
    model = Vizit
    form_class = VizitForm
        
    def get_success_url(self):
        return reverse("Vizit:home")

    def get_initial(self):
        us = Kam.objects.filter( siteuser= self.request.user )
        try:
            inituser = us[0].pk
        except:
            inituser =''
        
        
        self.initial.update({'kamid': inituser})
        return super(VizitCreate, self).get_initial()
    
    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(VizitCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class VizitDelete (LoginRequiredMixin,DeleteView):
    model = Vizit
    #form_class = VizitForm
        
    def get_success_url(self):
        return reverse("Vizit:home")
    
    def get_context_data(self, **kwargs):
                
        obj = super(VizitDelete, self).get_object()    
        print(obj.contact)
        ctx = super(VizitDelete, self).get_context_data(**kwargs)
        ctx['delcontact'] = obj
        return ctx
    
class VizitDeleteTest (DeleteView):
    model = Vizit
    #form_class = VizitForm
        
    def get_success_url(self):
        return reverse("Vizit:home")
    
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(VizitDelete, self).get_object()
        us = Kam.objects.filter( siteuser= self.request.user )
        
        try:
            inituser = us[0].pk
        except:
            inituser =''
        
        print (self.request.user)
        print (inituser)
        print (obj.kamid)
        
        if obj.kamid != inituser:
            print(':::::: не владелец')
            raise Http404
        
        print(self.request.user)
        return obj

    
class ContactCreate (LoginRequiredMixin,CreateView):
   
    model = Contact
    fields= ['name','spec','phone','email','city','kam','cat_filler_potencial','cat_filler_loyalty','cat_biostim_potencial','cat_biostim_loyalty','cat_idp_potencial','cat_idp_loyalty','work_place','comment','name_dashboard']

    def get_success_url(self):
        return reverse("Vizit:home")

class ContactAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        if not self.request.user.is_authenticated:
            return Contact.objects.none()

        qs = Contact.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

def getrabota(request):

    if request.user.is_authenticated == False :
        return HttpResponseRedirect("/accounts/login")


    q=request.GET['work']
    qs = Contact.objects.get(id=q)
    
    res = {"work":qs.work_place,"spec":qs.spec,"category":qs.category_account}
    return JsonResponse(res)

def gethi3nt(request):

    if request.user.is_authenticated == False :
        return HttpResponseRedirect("/accounts/login")

    q=request.GET['work']
    print(q)
    qs = Contact.objects.get(id=q)
    
    #res = str(qs.work_place)+ '|'+ str(qs.spec)+'|'+str(qs.category_account)
    res = qs.work_place
    print (res)
    res= "dsa"
    return HTTPResponse(res)

def gethint(request):

    if request.user.is_authenticated == False :
        return HttpResponseRedirect("/accounts/login")

    q=request.GET['id']
    try:
        qs = Contact.objects.get(id=q)
        res = str(qs.work_place)+ '|'+ str(qs.spec)+'|'+str(qs.category_account)
    except:
        res=''
    return HttpResponse(res)

def calculon(calc_year, calc_month):

    allfreq = VizitFreq.objects.filter(year =calc_year, month =calc_month)
    
    #FreqByMonth = {1:5,2:5,3:5,4:5,5:5,6:5,7:8,8:8,9:8,10:8,11:8,12:8}

    for freq in allfreq:
        
        #nowfreq = FreqByMonth[freq.month]
        nowfreq=8
        
        freq.dayadm_minus= (freq.workdays - nz0(freq.dayoff_minus))/8
        freq.workday_count = freq.workdays - nz0(freq.dayoff_minus) - freq.dayadm_minus

        cnt= Contact.objects.filter(kam=freq.kamid, category_account='A')
        freq.contact_count_a = cnt.count()
        #freq.plan_count_a = cnt.count()*2
        freq.plan_count_a = cnt.count()*1

        datebegin = datetime.date(calc_year,freq.month,1)
        
        dateend = datebegin + relativedelta(months=+1)
        

        fact= Vizit.objects.filter(datefact__gte=datebegin,datefact__lt=dateend,kamid=freq.kamid, contact__in =cnt)
        #fact= Vizit.objects.filter(kamid=freq.kamid, contact__in =cnt)
        freq.fact_count_a= fact.count()


        if freq.workday_count*nowfreq<=freq.plan_count_a:
            freq.plan_count_a=freq.workday_count*nowfreq

        freq.freq_a = freq.plan_count_a/freq.workday_count


        cnt= Contact.objects.filter(kam=freq.kamid, category_account='B')
        freq.contact_count_b = cnt.count()
        freq.plan_count_b = cnt.count()

        fact= Vizit.objects.filter(datefact__gte=datebegin,datefact__lt=dateend,kamid=freq.kamid, contact__in =cnt)
        freq.fact_count_b= fact.count()

        if freq.plan_count_a <=freq.workday_count*nowfreq:
            if freq.plan_count_a+freq.plan_count_b>=freq.workday_count*nowfreq:
                freq.plan_count_b=freq.workday_count*nowfreq-freq.plan_count_a
        else:
            freq.plan_count_b=0
        
        freq.freq_b = freq.plan_count_b/freq.workday_count

                

        cnt= Contact.objects.filter(kam=freq.kamid, category_account='C')
        freq.contact_count_c = cnt.count()
        freq.plan_count_c = cnt.count()

        fact= Vizit.objects.filter(datefact__gte=datebegin,datefact__lt=dateend,kamid=freq.kamid, contact__in =cnt)
        freq.fact_count_c= fact.count()

        if freq.plan_count_a+freq.plan_count_b <=freq.workday_count*nowfreq:
            if freq.plan_count_a+freq.plan_count_b+freq.plan_count_c>=freq.workday_count*nowfreq:
                freq.plan_count_c=freq.workday_count*nowfreq-freq.plan_count_a-freq.plan_count_b
        else:
            freq.plan_count_c=0
        

        freq.freq_c = freq.plan_count_c/freq.workday_count


        freq.freq_total = freq.freq_a+freq.freq_b+freq.freq_c


        freq.dayoff_minus=nz0(freq.dayoff_minus)
        freq.kamname = Kam.objects.get(id=freq.kamid.id).name

        if freq.plan_count_a==0:
            freq.procent_a=0
        else:
            freq.procent_a=freq.fact_count_a/freq.plan_count_a*100

        if freq.plan_count_b==0:
            freq.procent_b=0
        else:
            freq.procent_b=freq.fact_count_b/freq.plan_count_b*100

        if freq.plan_count_c==0:
            freq.procent_c=0
        else:
            freq.procent_c=freq.fact_count_c/freq.plan_count_c*100

        freq.save()
    

def nz0(value):
    return int(0 if value is None else value)

def initinsert(request):
    
    workdaysmonth={10:22,11:21,12:21}
    for wm in workdaysmonth:
        for km in [4,5,11]:

            a= VizitFreq()
            a.kamid=Kam.objects.get(id=km)
            a.year= 2023
            a.month=wm
            a.workdays=workdaysmonth[wm]
            a.save()
    return HttpResponse('')


class EventCreateView(CreateView):
    model = Event
    fields = [ "goal","dateevent","result","kamid","topic","city"]
    

    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["children"] = MemberFormset(self.request.POST)
        else:
            data["children"] = MemberFormset()
        return data

    
    def form_valid(self, form):
       
        context = self.get_context_data()
        children = context["children"]
        self.object = form.save()
        if children.is_valid():
            children.instance = self.object
            children.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("Vizit:EventList")



class EventUpdateView(UpdateView):
    model = Event
    fields = ["dateevent", "goal", "result","kamid","topic","city"]
    #form_class = EventForm
    
    def get_context_data(self, **kwargs):

        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["children"] = MemberFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data["children"] = MemberFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()

        children = context["children"]

        self.object = form.save()
        if children.is_valid():
            
            children.instance = self.object
            children.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("Vizit:EventList")

class EventList (LoginRequiredMixin, ListView):
    context_object_name = 'Event'
    model = Event
    paginate_by = 30

class TestView(TemplateView):
    template_name = 'vizit/test.html'
