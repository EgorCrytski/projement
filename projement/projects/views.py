import os

from django.db.models import F
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from markdown import markdown

from projects.forms import ProjectForm, LogForm
from projects.models import Project, Log


def LogChanges(request, pk):
    project = get_object_or_404(Project, id=pk)
    log = Log()
    if request.method == "POST":
        form = LogForm(request.POST)
        if form.is_valid():
            log.user = get_object_or_404(User, id=request.user.id)
            log.project = project
            log.initial_design = project.actual_design
            log.initial_development = project.actual_development
            log.initial_testing = project.actual_testing
            project.actual_design += form.cleaned_data['actual_design']
            project.actual_development += form.cleaned_data['actual_development']
            project.actual_testing += form.cleaned_data['actual_testing']
            log.result_design = project.actual_design
            log.result_development = project.actual_development
            log.result_testing = project.actual_testing
            project.save()
            log.save()
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = LogForm(initial={'actual_design': 0, 'actual_development': 0, 'actual_testing': 0})

    return render(request, 'projects/project_form.html', {'form': form})


class AssignmentView(TemplateView):
    template_name = 'projects/assignment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with open(os.path.join(os.path.dirname(settings.BASE_DIR), 'README.md'), encoding='utf-8') as f:
            assignment_content = f.read()

        context.update({
            'assignment_content': mark_safe(markdown(assignment_content))
        })

        return context


class DashboardView(LoginRequiredMixin, ListView):
    model = Project
    ordering = ('-end_date',)
    context_object_name = 'projects'
    template_name = 'projects/dashboard.html'

    def get_queryset(self):
        projects = super().get_queryset()
        projects = projects.select_related('company')
        return projects


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.actual_design += F('actual_design')
        form.instance.actual_development += F('actual_development')
        form.instance.actual_testing += F('actual_testing')
        return super().form_valid(form)


class LogView(LoginRequiredMixin, ListView):
    model = Log
    context_object_name = 'log'
    template_name = 'projects/log.html'

    def get_queryset(self):
        log = super().get_queryset()
        log = log.select_related('user')
        return log


class LogCreateView(LoginRequiredMixin, CreateView):
    model = Log
    context_object_name = 'log'
    form_class = ProjectForm
