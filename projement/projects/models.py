from decimal import Decimal

from django.core.validators import MinValueValidator
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
    company = models.ForeignKey('projects.Company', on_delete=models.PROTECT, related_name='projects')

    title = models.CharField('Project title', max_length=128)
    start_date = models.DateField('Project start date', blank=True, null=True)
    end_date = models.DateField('Project end date', blank=True, null=True)

    estimated_design = models.DecimalField('Estimated design hours', max_digits=5, decimal_places=1,
                                           validators=[MinValueValidator(Decimal('0.01'))])
    actual_design = models.DecimalField('Actual design hours', default=0, decimal_places=1, max_digits=5,
                                        validators=[MinValueValidator(Decimal('0.01'))])

    estimated_development = models.DecimalField('Estimated development hours', max_digits=5, decimal_places=1,
                                                validators=[MinValueValidator(Decimal('0.01'))])
    actual_development = models.DecimalField('Actual development hours', default=0, decimal_places=1, max_digits=5,
                                             validators=[MinValueValidator(Decimal('0.01'))])

    estimated_testing = models.DecimalField('Estimated testing hours', max_digits=5, decimal_places=1,
                                            validators=[MinValueValidator(Decimal('0.01'))])
    actual_testing = models.DecimalField('Actual testing hours', default=0, decimal_places=1, max_digits=5,
                                         validators=[MinValueValidator(Decimal('0.01'))])

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
    project = models.ForeignKey('Project', on_delete=models.PROTECT)
    user = models.ForeignKey('auth.user', on_delete=models.PROTECT)

    initial_design = models.DecimalField('Initial design hours', default=0, max_digits=5, decimal_places=1,
                                         validators=[MinValueValidator(Decimal('0.01'))])

    result_design = models.DecimalField('Result design hours', default=0, decimal_places=1, max_digits=5,
                                        validators=[MinValueValidator(Decimal('0.01'))])

    initial_development = models.DecimalField('Initial development hours', default=0, max_digits=5, decimal_places=1,
                                              validators=[MinValueValidator(Decimal('0.01'))])

    result_development = models.DecimalField('Result development hours', default=0, decimal_places=1, max_digits=5,
                                             validators=[MinValueValidator(Decimal('0.01'))])

    initial_testing = models.DecimalField('Initial testing hours', default=0, max_digits=5, decimal_places=1,
                                          validators=[MinValueValidator(Decimal('0.01'))])

    result_testing = models.DecimalField('Result testing hours', default=0, decimal_places=1, max_digits=5,
                                         validators=[MinValueValidator(Decimal('0.01'))])

    @property
    def delta_design(self):
        return self.result_design - self.initial_design

    @property
    def delta_development(self):
        return self.result_development - self.initial_development

    @property
    def delta_testing(self):
        return self.result_testing - self.initial_testing
