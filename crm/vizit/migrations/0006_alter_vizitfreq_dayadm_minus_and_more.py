# Generated by Django 4.0.3 on 2022-04-22 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vizit', '0005_alter_vizitfreq_contact_count_a_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vizitfreq',
            name='dayadm_minus',
            field=models.FloatField(blank=True, null=True, verbose_name='Колво дней административной работы'),
        ),
        migrations.AlterField(
            model_name='vizitfreq',
            name='dayoff_minus',
            field=models.IntegerField(blank=True, null=True, verbose_name='Колво выходных у сотрудника'),
        ),
        migrations.AlterField(
            model_name='vizitfreq',
            name='workdays',
            field=models.IntegerField(blank=True, null=True, verbose_name='Колво рабочих дней в месяце'),
        ),
    ]
