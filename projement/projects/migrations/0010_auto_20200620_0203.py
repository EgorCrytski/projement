# Generated by Django 2.2 on 2020-06-19 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20200620_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttag',
            name='attach_date',
            field=models.DateField(auto_now=True, verbose_name='Date of attachment'),
        ),
    ]
