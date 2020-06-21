# Generated by Django 2.2 on 2020-06-19 22:31

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20200618_0251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=16, verbose_name='Tag name')),
            ],
        ),
        migrations.AlterField(
            model_name='log',
            name='initial_design',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Initial design hours'),
        ),
        migrations.AlterField(
            model_name='log',
            name='initial_development',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Initial development hours'),
        ),
        migrations.AlterField(
            model_name='log',
            name='initial_testing',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Initial testing hours'),
        ),
        migrations.AlterField(
            model_name='log',
            name='result_design',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Result design hours'),
        ),
        migrations.AlterField(
            model_name='log',
            name='result_development',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Result development hours'),
        ),
        migrations.AlterField(
            model_name='log',
            name='result_testing',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Result testing hours'),
        ),
        migrations.CreateModel(
            name='ProjectsTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attach_date', models.DateField(verbose_name='Date of attachment')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projects.Project')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projects.Tag')),
            ],
        ),
    ]