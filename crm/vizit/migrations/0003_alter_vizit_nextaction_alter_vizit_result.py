# Generated by Django 4.0.3 on 2022-04-08 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vizit', '0002_vizit_vizstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vizit',
            name='nextaction',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True, verbose_name='Дальнейшие действия с клиентом'),
        ),
        migrations.AlterField(
            model_name='vizit',
            name='result',
            field=models.CharField(blank=True, choices=[('Cold', 'Cold'), ('Warm', 'Warm'), ('Hot', 'Hot')], max_length=10, null=True, verbose_name='Результат визита (личная оценка)'),
        ),
    ]
