from django.conf.urls import url

from projects.views import AssignmentView, DashboardView, ProjectUpdateView, LogView, LogChanges

urlpatterns = [
    url(r'^$', AssignmentView.as_view(), name='assignment'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^log/$', LogView.as_view(), name='log'),
    # url(r'^projects/(?P<pk>[0-9]+)-(?P<slug>[-\w]*)/$', ProjectUpdateView.as_view(), name='project-update'),
    url(r'^projects/(?P<pk>[0-9]+)/$', LogChanges, name='project-update'),
]
