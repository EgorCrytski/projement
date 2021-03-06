from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from projects.views import AssignmentView, DashboardView, ProjectUpdateView, LogView, log_changes, export_xls

urlpatterns = [
    url(r'^$', AssignmentView.as_view(), name='assignment'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^log/$', LogView.as_view(), name='log'),
    # url(r'^projects/(?P<pk>[0-9]+)-(?P<slug>[-\w]*)/$', ProjectUpdateView.as_view(), name='project-update'),
    url(r'^projects/(?P<pk>[0-9]+)/$', login_required(log_changes), name='project-update'),
    url(r'^xls/$', login_required(export_xls), name='export_xls'),
]
