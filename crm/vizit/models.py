from django.db import models

# Create your models here.

class Vizit(models.Model):

    result_choise=[('Cold', 'Cold'),('Warm', 'Warm'),('Hot', 'Hot')]
    type_choise= [('К специалисту', 'К специалисту'),('Follow-up визит', 'Follow-up визит'),('Телефонный визит', 'Телефонный визит')]
    status_choise= [('Открыт', 'Открыт'),('Закрыт', 'Закрыт')]

    viztype = models.CharField(max_length=20, verbose_name='Тип визита', choices=type_choise)
    vizstatus = models.CharField(max_length=20, verbose_name='Статус', choices=status_choise, default='Открыт')
    datenext = models.DateTimeField(blank=True,null=True, db_index = True, verbose_name='Дата следующего визита')
    datefact = models.DateTimeField(auto_now_add = False, db_index = True, verbose_name='Дата визита')
    goal = models.CharField (max_length=200, db_index=True, verbose_name='Цель визита')
    nextaction = models.CharField (blank=True,null=True, max_length=200, db_index=True, verbose_name='Дальнейшие действия с клиентом')
    social_link = models.BooleanField (blank=True, null = True, verbose_name='Подписание клиента на соцсети')
    result = models.CharField(blank=True, null=True, max_length=10, verbose_name='Результат визита (личная оценка)', choices=result_choise)
    contact = models.ForeignKey ('Contact', null = True, on_delete=models.PROTECT, verbose_name='Контакт')
    comment  = models.TextField(blank=True, null=True,  verbose_name='Комментарий')
    kamid = models.ForeignKey('Kam',on_delete=models.PROTECT, verbose_name='Сотрудник')
    hint_organization = models.CharField (blank=True, null = True, max_length=200, db_index=True, verbose_name='Место работы')
    hint_special = models.CharField (blank=True, null = True, max_length=200, db_index=True, verbose_name='Специальность')
    datecreate = models.DateTimeField(auto_now_add = True, db_index = True, verbose_name='Дата создания')

    class Meta:
        verbose_name_plural = 'Визиты'
        verbose_name = 'Визит'
    
    def __str__(self) -> str:
        return self.kamid.name + ' ' + self.viztype


class Kam(models.Model):
    name  = models.CharField(max_length=250, verbose_name='Фио сотрудника')
    siteuser = models.CharField(max_length=250, verbose_name='Логин на сайте')

    class Meta:
        verbose_name_plural = 'Сотрудники'
        verbose_name = 'Сотрудник'
    
    def __str__(self) -> str:
        return self.name 

class Contact(models.Model):
    cat1=[('A', 'A'),('B', 'B'),('C', 'C'),('D', 'D')]
    cat2=[('0', '0'),('1', '1'),('2', '2'),('3', '3')]
    cat3=[('L-D', 'L-D'),('LOW', 'LOW'),('MID', 'MID'),('TOP', 'TOP')]
    cat4=[('LD', 'LD'),('LOW', 'LOW'),('MID', 'MID'),('TOP', 'TOP')]
    
    special = [
    ('дерматолог-косметолог','дерматолог-косметолог'),
    ('пластический хирург','пластический хирург'),
    ('Администратор','Администратор'), 
    ('Другое','Другое'),
    ('Гл.врач','Гл.врач')
    ]

    name  = models.CharField(max_length=250, verbose_name='Фио врача')
    spec  = models.CharField(max_length=250, verbose_name='Специальность', choices=special)
    phone = models.CharField(null=True, blank = True, max_length=250, verbose_name='Телефон')
    email = models.CharField(null=True, blank = True, max_length=250, verbose_name='Email')
    
    category_account = models.CharField(null=True, blank = True,max_length=12, verbose_name='Account Cat', choices=cat1)
    category_restylane = models.CharField(null=True, blank = True,max_length=12, verbose_name='Restylane loyalty', choices=cat2)
    category_sculptra = models.CharField(null=True, blank = True,max_length=12, verbose_name='Sculptra Cat', choices=cat3)
    
    cat_filler_potencial =models.CharField(null=True, blank = True,max_length=12, verbose_name='Fillers Category Potencial', choices=cat1)
    cat_filler_loyalty =models.CharField(null=True, blank = True,max_length=12, verbose_name='Fillers Loyalty', choices=cat2)

    cat_biostim_potencial =models.CharField(null=True, blank = True,max_length=12, verbose_name='Biostimulators Category Potential', choices=cat4)
    cat_biostim_loyalty =models.CharField(null=True, blank = True,max_length=12, verbose_name='Biostimulators Loyalty', choices=cat2)

    cat_idp_potencial =models.CharField(null=True, blank = True,max_length=12, verbose_name='IDP Category', choices=cat1)
    cat_idp_loyalty =models.CharField(null=True, blank = True,max_length=12, verbose_name='IDP Loyalty', choices=cat2)


    city   = models.CharField(max_length=250, verbose_name='Город')
    kam = models.ForeignKey ('Kam', null = True, on_delete=models.PROTECT, verbose_name='КАМ')
    work_place = models.CharField(max_length=250, verbose_name='Место работы')
    comment = models.CharField(null=True, blank = True, max_length=250, verbose_name='Комментарий')
    name_dashboard = models.CharField(null=True, blank = True, max_length=250, verbose_name='Наименование в DB')
    date_create = models.DateTimeField(auto_now_add = True, verbose_name='Дата создания')
    deleted = models.BooleanField(default=False, verbose_name='Контакт удален')

    def category(self):
        res =""
        if self.cat_filler_potencial is not None:
            res+= self.cat_filler_potencial 
        if self.cat_filler_loyalty is not None:
            res+= self.cat_filler_loyalty

        if self.cat_biostim_potencial is not None:
            res+= self.cat_biostim_potencial 
        if self.cat_biostim_loyalty is not None:
            res+= self.cat_biostim_loyalty 

        if self.cat_idp_potencial is not None:
            res+= self.cat_idp_potencial 
        if self.cat_idp_loyalty is not None:
            res+= self.cat_idp_loyalty 
        
        return res
        
    
    def __str__(self) -> str:
        return self.name       

    class Meta:
        verbose_name_plural = 'Контакты'
        verbose_name = 'Контакт'

class VizitFreq(models.Model):
    year=models.IntegerField(verbose_name="Год")
    month=models.IntegerField(verbose_name="Месяц")
    kamid = models.ForeignKey ('Kam', null = True, on_delete=models.PROTECT, verbose_name='КАМ')
    workdays=models.IntegerField(verbose_name="Дней в месяце",null=True, blank = True)
    dayoff_minus=models.IntegerField(verbose_name="Выходные",null=True, blank = True)
    dayadm_minus=models.FloatField(verbose_name="Адм. работа",null=True, blank = True)
    workday_count=models.FloatField(verbose_name="Дней работы",null=True, blank = True)
    contact_count_a=models.IntegerField(verbose_name="Колво врачей А",null=True, blank = True)
    contact_count_b=models.IntegerField(verbose_name="Колво врачей B",null=True, blank = True)
    contact_count_c=models.IntegerField(verbose_name="Колво врачей C",null=True, blank = True)
    plan_count_a=models.IntegerField(verbose_name="План визитов А",null=True, blank = True)
    plan_count_b=models.IntegerField(verbose_name="План визитов B",null=True, blank = True)
    plan_count_c=models.IntegerField(verbose_name="План визитов C",null=True, blank = True)
    freq_a=models.FloatField(verbose_name="Частота А",null=True, blank = True)
    freq_b=models.FloatField(verbose_name="Частота B",null=True, blank = True)
    freq_c=models.FloatField(verbose_name="Частота C",null=True, blank = True)
    freq_total=models.FloatField(verbose_name="Частота C",null=True, blank = True)
    kamname  = models.CharField(max_length=250, verbose_name='Фио kam',null=True, blank = True)
    fact_count_a=models.IntegerField(verbose_name="Факт визитов А",null=True, blank = True)
    fact_count_b=models.IntegerField(verbose_name="Факт визитов B",null=True, blank = True)
    fact_count_c=models.IntegerField(verbose_name="Факт визитов C",null=True, blank = True)
    
    procent_a=models.FloatField(verbose_name="% А",null=True, blank = True)
    procent_b=models.FloatField(verbose_name="% B",null=True, blank = True)
    procent_c=models.FloatField(verbose_name="% C",null=True, blank = True)
    
    def __str__(self) -> str:
        return str(self.month) +'/'+ str(self.year) +'/'+ self.kamname + ' ID строки:' + str(self.pk) 
    
    class Meta:
        verbose_name_plural = 'Частота визитов'
        verbose_name = 'Частота визитов'

class Event(models.Model):

    kamid = models.ForeignKey(Kam,on_delete=models.PROTECT, verbose_name='Сотрудник')
    dateevent = models.DateTimeField(auto_now_add = False, db_index = True, verbose_name='Дата мероприятия')
    
    topic = models.ForeignKey ('EventTopic', on_delete=models.PROTECT,db_index=True, verbose_name='Тема мероприятия')
    result = models.CharField(blank=True, null=True, max_length=255, verbose_name='Результат')
    goal = models.CharField(blank=True, null=True, max_length=255, verbose_name='Цель')
    city = models.CharField(blank=True, null=True, max_length=255, verbose_name='Город')

    class Meta:
        verbose_name_plural = 'Мероприятие'
        verbose_name = 'Мероприятия'
    
class EventTopic(models.Model):
    topicname = models.CharField (max_length=200, db_index=True, verbose_name='Тема мероприятия')
    
    def __str__(self) -> str:
        return self.topicname   

    class Meta:
        verbose_name_plural = 'Тема мероприятия'
        verbose_name = 'Темы мероприятий'


class EventMember(models.Model):
    parentevent = models.ForeignKey(Event, on_delete=models.CASCADE)
    contact = models.ForeignKey (Contact, null = True, on_delete=models.PROTECT, verbose_name='Контакт')
    
    class Meta:
        verbose_name = 'Участник мероприятия'
        verbose_name_plural = 'Участники мероприятия'
