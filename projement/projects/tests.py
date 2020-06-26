from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.test import Client, TestCase
from projects.forms import LogForm
from projects.models import Project


class DashboardTestCase(TestCase):
    fixtures = ['projects/fixtures/initial.json']

    def setUp(self):
        super().setUp()

        username, password = 'Thorgate', 'thorgate123'
        User.objects.create_user(username=username, email='info@throgate.eu', password=password)

        self.authenticated_client = Client()
        self.authenticated_client.login(username=username, password=password)

    def test_dashboard_requires_authentication(self):
        # Anonymous users can't see the dashboard

        client = Client()
        response = client.get('/dashboard/')
        self.assertRedirects(response, '/login/?next=/dashboard/')

        # Authenticated users can see the dashboard

        response = self.authenticated_client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_projects_on_dashboard(self):
        # There are 3 projects on the dashboard (loaded from the fixtures)

        response = self.authenticated_client.get('/dashboard/')
        projects = response.context['projects']
        self.assertEqual(len(projects), 3)

    def test_projects_ordering(self):
        response = self.authenticated_client.get('/dashboard/')
        projects = response.context['projects']
        self.assertEqual(projects[0].title, 'Projement')

    def test_get_xls_unauthorized(self):
        client = Client()
        response = client.get('/xls/')
        self.assertEqual(response.status_code, 302)

    def test_get_xls_authorized(self):
        response = self.authenticated_client.get('/xls/')
        self.assertEqual(response.status_code, 200)

    def test_get_log_unauthorized(self):
        client = Client()
        response = client.get('/log/')
        self.assertEqual(response.status_code, 302)

    def test_get_log_authorized(self):
        response = self.authenticated_client.get('/log/')
        self.assertEqual(response.status_code, 200)

    '''def test_change_record(self):
        print(Project.objects.get(id = 1).actual_design)
        form = LogForm(initial={'actual_design': 5, 'actual_development': 5, 'actual_testing': 5})
        response = self.authenticated_client.post('/projects/1', data= form.data)
        print(Project.objects.get(id=1).actual_design)
        self.assertEqual(response.status_code, 301)
        '''





class FormTestCase(TestCase):

    def test_validation(self):
        data = {'actual_design': '-5', 'actual_development': '-5', 'actual_testing': '-5'}
        form = LogForm(data)
        self.assertFalse(form.is_valid())

        data = {'actual_design': '5', 'actual_development': '5', 'actual_testing': '5'}
        form = LogForm(data)
        self.assertTrue(form.is_valid())

        data = {'actual_design': '99999', 'actual_development': '99999', 'actual_testing': '99999'}
        form = LogForm(data)
        self.assertFalse(form.is_valid())


class ProjectsTestCase(TestCase):
    fixtures = ['projects/fixtures/initial.json']

    def setUp(self):
        super().setUp()

        self.projects = Project.objects.order_by('id')

    def test_project_has_ended(self):
        # 2 of the projects have ended
        self.assertListEqual([p.has_ended for p in self.projects], [True, True, False])

    def test_project_is_over_budget(self):
        # 1 of the projects is over budget
        self.assertListEqual([p.is_over_budget for p in self.projects], [True, False, False])

    def test_total_estimated_hours(self):
        self.assertListEqual([p.total_estimated_hours for p in self.projects], [690, 170, 40])

    def test_total_actual_hours(self):
        self.assertListEqual([p.total_actual_hours for p in self.projects], [739, 60, 5])
