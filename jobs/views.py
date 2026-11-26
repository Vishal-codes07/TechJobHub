from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import JobForm
from .models import Application, Job


# --------------------------------------------------------------------------
# Permission helpers
# --------------------------------------------------------------------------
class FriendlyPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Login required + a friendly redirect (instead of a bare 403 page)."""

    denied_message = 'You do not have permission to do that.'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, self.denied_message)
        return redirect('job_list')


class EmployerRequiredMixin(FriendlyPermissionMixin):
    denied_message = 'Only employer accounts can do that.'

    def test_func(self):
        return self.request.user.role == 'employer'


class JobOwnerRequiredMixin(FriendlyPermissionMixin):
    """Only the employer who posted the job may change it."""

    denied_message = 'You can only manage job postings that you created.'

    def test_func(self):
        return self.get_object().posted_by_id == self.request.user.pk


# --------------------------------------------------------------------------
# Public views
# --------------------------------------------------------------------------
class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 6

    def get_queryset(self):
        qs = Job.objects.select_related('posted_by')
        q = self.request.GET.get('q', '').strip()
        location = self.request.GET.get('location', '').strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(company_name__icontains=q) | Q(description__icontains=q)
            )
        if location:
            qs = qs.filter(location__icontains=location)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop('page', None)
        ctx['q'] = self.request.GET.get('q', '').strip()
        ctx['location'] = self.request.GET.get('location', '').strip()
        ctx['querystring'] = params.urlencode()
        ctx['total_jobs'] = ctx['paginator'].count
        return ctx


class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_details.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx['has_applied'] = (
            user.is_authenticated
            and Application.objects.filter(job=self.object, applicant=user).exists()
        )
        ctx['is_owner'] = user.is_authenticated and self.object.posted_by_id == user.pk
        ctx['applicant_count'] = self.object.application_set.count() if ctx['is_owner'] else None
        return ctx


# --------------------------------------------------------------------------
# Employer views
# --------------------------------------------------------------------------
class JobCreateView(EmployerRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('my_jobs')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        messages.success(self.request, 'Your job posting was created.')
        return super().form_valid(form)


class JobUpdateView(JobOwnerRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    context_object_name = 'job'
    success_url = reverse_lazy('my_jobs')

    def form_valid(self, form):
        messages.success(self.request, 'Your job posting was updated.')
        return super().form_valid(form)


class JobDeleteView(JobOwnerRequiredMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    context_object_name = 'job'
    success_url = reverse_lazy('my_jobs')

    def form_valid(self, form):
        messages.success(self.request, 'Your job posting was deleted.')
        return super().form_valid(form)


class MyJobsListView(EmployerRequiredMixin, ListView):
    model = Job
    template_name = 'jobs/my_jobs.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user).annotate(
            applicant_count=Count('application')
        )


class JobApplicantsView(JobOwnerRequiredMixin, DetailView):
    model = Job
    template_name = 'jobs/job_applicants.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['applications'] = (
            Application.objects.filter(job=self.object)
            .select_related('applicant')
            .order_by('-date_applied', '-pk')
        )
        return ctx


# --------------------------------------------------------------------------
# Job seeker views
# --------------------------------------------------------------------------
@login_required
def apply_to_job(request, pk):
    if request.method != 'POST':
        return redirect('job_detail', pk=pk)

    job = get_object_or_404(Job, pk=pk)

    if request.user.role != 'seeker':
        messages.error(request, 'Only job seeker accounts can apply to jobs.')
        return redirect('job_detail', pk=job.pk)

    _, created = Application.objects.get_or_create(job=job, applicant=request.user)
    if created:
        messages.success(request, f'Your application for “{job.title}” was submitted.')
    else:
        messages.info(request, 'You have already applied to this job.')
    return redirect('job_detail', pk=job.pk)


class MyApplicationsListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'jobs/my_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return (
            Application.objects.filter(applicant=self.request.user)
            .select_related('job')
            .order_by('-date_applied', '-pk')
        )
