from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Company(models.Model):
    class Meta:
        verbose_name_plural = "companies"

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Project(models.Model):
    company = models.ForeignKey('projects.Company', on_delete=models.CASCADE, related_name='projects')

    title = models.CharField('Project title', max_length=128)
    start_date = models.DateField('Project start date', blank=True, null=True)
    end_date = models.DateField('Project end date', blank=True, null=True)

    estimated_design = models.DecimalField('Estimated design hours', max_digits=7, decimal_places=2,
                                           validators=[MinValueValidator(Decimal('0.01')),
                                                       MaxValueValidator(Decimal('9999.99'))])
    actual_design = models.DecimalField('Actual design hours', default=0, decimal_places=2, max_digits=7,
                                        validators=[MinValueValidator(Decimal('0')),
                                                    MaxValueValidator(Decimal('9999.99'))])

    estimated_development = models.DecimalField('Estimated development hours', max_digits=7, decimal_places=2,
                                                validators=[MinValueValidator(Decimal('0.01')),
                                                            MaxValueValidator(Decimal('9999.99'))])
    actual_development = models.DecimalField('Actual development hours', default=0, decimal_places=2, max_digits=7,
                                             validators=[MinValueValidator(Decimal('0')),
                                                         MaxValueValidator(Decimal('9999.99'))])

    estimated_testing = models.DecimalField('Estimated testing hours', max_digits=7, decimal_places=2,
                                            validators=[MinValueValidator(Decimal('0.01')),
                                                        MaxValueValidator(Decimal('9999.99'))])
    actual_testing = models.DecimalField('Actual testing hours', default=0, decimal_places=2, max_digits=7,
                                         validators=[MinValueValidator(Decimal('0')),
                                                     MaxValueValidator(Decimal('9999.99'))])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-update', kwargs={'pk': self.pk})

    @property
    def has_ended(self):
        return self.end_date is not None and self.end_date < timezone.now().date()

    @property
    def total_estimated_hours(self):
        return self.estimated_design + self.estimated_development + self.estimated_testing

    @property
    def total_actual_hours(self):
        return self.actual_design + self.actual_development + self.actual_testing

    @property
    def is_over_budget(self):
        return self.total_actual_hours > self.total_estimated_hours


class Log(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)

    initial_design = models.DecimalField('Initial design hours', default=0, max_digits=7, decimal_places=2,
                                         validators=[MinValueValidator(Decimal('0')),
                                                     MaxValueValidator(Decimal('9999.99'))])

    result_design = models.DecimalField('Result design hours', default=0, decimal_places=2, max_digits=7,
                                        validators=[MinValueValidator(Decimal('0')),
                                                    MaxValueValidator(Decimal('9999.99'))])

    initial_development = models.DecimalField('Initial development hours', default=0, max_digits=7, decimal_places=2,
                                              validators=[MinValueValidator(Decimal('0')),
                                                          MaxValueValidator(Decimal('9999.99'))])

    result_development = models.DecimalField('Result development hours', default=0, decimal_places=2, max_digits=7,
                                             validators=[MinValueValidator(Decimal('0')),
                                                         MaxValueValidator(Decimal('9999.99'))])

    initial_testing = models.DecimalField('Initial testing hours', default=0, max_digits=7, decimal_places=2,
                                          validators=[MinValueValidator(Decimal('0')),
                                                      MaxValueValidator(Decimal('9999.99'))])

    result_testing = models.DecimalField('Result testing hours', default=0, decimal_places=2, max_digits=7,
                                         validators=[MinValueValidator(Decimal('0')),
                                                     MaxValueValidator(Decimal('9999.99'))])

    def __str__(self):
        return self.project.title + ': ' + self.user.username

    @property
    def delta_design(self):
        return self.result_design - self.initial_design

    @property
    def delta_development(self):
        return self.result_development - self.initial_development

    @property
    def delta_testing(self):
        return self.result_testing - self.initial_testing


class Tag(models.Model):
    tagname = models.CharField('Tag name', max_length=16)
    project = models.ManyToManyField('Project', through='ProjectTag', related_name='tags')

    def __str__(self):
        return self.tagname


class ProjectTag(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    attach_date = models.DateField('Date of attachment', auto_now=True)

    def __str__(self):
        return self.project.title + ': ' + self.tag.tagname

    def get_attach_date(self):
        return self.attach_date
