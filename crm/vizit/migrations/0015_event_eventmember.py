# Generated by Django 4.0.3 on 2022-05-23 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vizit', '0014_contact_date_create'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(db_index=True, verbose_name='Дата мероприятия')),
                ('goal', models.CharField(db_index=True, max_length=200, verbose_name='Цель мероприятия')),
                ('result', models.CharField(blank=True, max_length=255, null=True, verbose_name='Результат')),
            ],
        ),
        migrations.CreateModel(
            name='EventMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='vizit.contact', verbose_name='Контакт')),
                ('parentevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vizit.event')),
            ],
            options={
                'verbose_name': 'Участник мероприятия',
                'verbose_name_plural': 'Участники мероприятия',
            },
        ),
    ]
