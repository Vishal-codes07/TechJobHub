from django.urls import path

from . import views

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('create/', views.JobCreateView.as_view(), name='job_create'),
    path('my/jobs/', views.MyJobsListView.as_view(), name='my_jobs'),
    path('my/applications/', views.MyApplicationsListView.as_view(), name='my_applications'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('<int:pk>/edit/', views.JobUpdateView.as_view(), name='job_update'),
    path('<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),
    path('<int:pk>/apply/', views.apply_to_job, name='apply_to_job'),
    path('<int:pk>/applicants/', views.JobApplicantsView.as_view(), name='job_applicants'),
]
