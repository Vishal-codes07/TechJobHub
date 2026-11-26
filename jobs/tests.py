from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser

from .models import Application, Job


class PortalFlowTests(TestCase):
    def setUp(self):
        self.employer = CustomUser.objects.create_user('boss', 'b@x.com', 'pass12345', role='employer')
        self.other_employer = CustomUser.objects.create_user('boss2', 'b2@x.com', 'pass12345', role='employer')
        self.seeker = CustomUser.objects.create_user('sam', 's@x.com', 'pass12345', role='seeker')
        self.job = Job.objects.create(
            title='Django Dev', company_name='Acme', description='Build things.\nSecond line.',
            location='Gurugram', salary=500000, posted_by=self.employer,
        )

    # ---- public pages
    def test_home_redirects_to_jobs(self):
        self.assertRedirects(self.client.get('/'), reverse('job_list'), fetch_redirect_response=False)

    def test_job_list_and_search(self):
        r = self.client.get(reverse('job_list'))
        self.assertContains(r, 'Django Dev')
        self.assertContains(self.client.get(reverse('job_list'), {'q': 'django'}), 'Django Dev')
        self.assertNotContains(self.client.get(reverse('job_list'), {'q': 'plumber'}), 'Django Dev')
        self.assertNotContains(self.client.get(reverse('job_list'), {'location': 'Mumbai'}), 'Django Dev')

    def test_job_detail_page_renders(self):
        r = self.client.get(reverse('job_detail', args=[self.job.pk]))
        self.assertContains(r, 'Log in to apply')
        self.assertContains(r, 'Second line.')

    def test_login_and_signup_pages_render(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)
        self.assertEqual(self.client.get(reverse('signup')).status_code, 200)

    # ---- signup / login / logout
    def test_signup_creates_user_with_role_and_logs_in(self):
        r = self.client.post(reverse('signup'), {
            'username': 'newbie', 'email': 'n@x.com', 'role': 'employer',
            'password1': 'Str0ng!Pass_91', 'password2': 'Str0ng!Pass_91',
        })
        self.assertRedirects(r, reverse('job_list'))
        user = CustomUser.objects.get(username='newbie')
        self.assertEqual(user.role, 'employer')
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_redirects_to_job_list(self):
        r = self.client.post(reverse('login'), {'username': 'sam', 'password': 'pass12345'})
        self.assertRedirects(r, reverse('job_list'))

    def test_logout_via_post(self):
        self.client.login(username='sam', password='pass12345')
        r = self.client.post(reverse('logout'))
        self.assertRedirects(r, reverse('job_list'))
        self.assertNotIn('_auth_user_id', self.client.session)

    # ---- applying
    def test_seeker_can_apply_once(self):
        self.client.login(username='sam', password='pass12345')
        url = reverse('apply_to_job', args=[self.job.pk])
        self.client.post(url)
        self.client.post(url)
        self.assertEqual(Application.objects.filter(applicant=self.seeker, job=self.job).count(), 1)
        self.assertContains(self.client.get(reverse('job_detail', args=[self.job.pk])), 'You have applied')
        self.assertContains(self.client.get(reverse('my_applications')), 'Django Dev')

    def test_employer_cannot_apply(self):
        self.client.login(username='boss2', password='pass12345')
        self.client.post(reverse('apply_to_job', args=[self.job.pk]))
        self.assertEqual(Application.objects.count(), 0)

    def test_apply_requires_login(self):
        r = self.client.post(reverse('apply_to_job', args=[self.job.pk]))
        self.assertEqual(r.status_code, 302)
        self.assertIn('/accounts/login/', r['Location'])
        self.assertEqual(Application.objects.count(), 0)

    # ---- employer actions
    def test_employer_can_create_job(self):
        self.client.login(username='boss', password='pass12345')
        r = self.client.post(reverse('job_create'), {
            'title': 'QA Engineer', 'company_name': 'Acme', 'description': 'Test stuff',
            'location': 'Delhi', 'salary': '450000',
        })
        self.assertRedirects(r, reverse('my_jobs'))
        self.assertTrue(Job.objects.filter(title='QA Engineer', posted_by=self.employer).exists())

    def test_seeker_cannot_create_job(self):
        self.client.login(username='sam', password='pass12345')
        self.assertRedirects(self.client.get(reverse('job_create')), reverse('job_list'))
        self.assertRedirects(self.client.get(reverse('my_jobs')), reverse('job_list'))

    def test_only_owner_can_edit_delete_view_applicants(self):
        self.client.login(username='boss2', password='pass12345')
        for name in ('job_update', 'job_delete', 'job_applicants'):
            self.assertRedirects(self.client.get(reverse(name, args=[self.job.pk])), reverse('job_list'))
        self.client.post(reverse('job_delete', args=[self.job.pk]))
        self.assertTrue(Job.objects.filter(pk=self.job.pk).exists())

    def test_owner_can_edit_and_delete(self):
        self.client.login(username='boss', password='pass12345')
        r = self.client.post(reverse('job_update', args=[self.job.pk]), {
            'title': 'Senior Django Dev', 'company_name': 'Acme', 'description': 'x',
            'location': 'Gurugram', 'salary': '800000',
        })
        self.assertRedirects(r, reverse('my_jobs'))
        self.job.refresh_from_db()
        self.assertEqual(self.job.title, 'Senior Django Dev')
        self.client.post(reverse('job_delete', args=[self.job.pk]))
        self.assertFalse(Job.objects.filter(pk=self.job.pk).exists())

    def test_owner_sees_applicants(self):
        Application.objects.create(job=self.job, applicant=self.seeker)
        self.client.login(username='boss', password='pass12345')
        self.assertContains(self.client.get(reverse('job_applicants', args=[self.job.pk])), 'sam')
        self.assertContains(self.client.get(reverse('my_jobs')), '1 applicant')

    def test_pagination(self):
        for i in range(10):
            Job.objects.create(title=f'Role {i}', company_name='C', description='d', location='L',
                               salary=1, posted_by=self.employer)
        r = self.client.get(reverse('job_list'))
        self.assertTrue(r.context['is_paginated'])
        self.assertEqual(self.client.get(reverse('job_list'), {'page': 2}).status_code, 200)
