from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.getAllJobs, name='jobs'),
    path('jobs/new/', views.newJob, name='new_job'),
    path('jobs/<str:pk>/', views.getJob, name='job'),
    path('jobs/<str:pk>/update/', views.updateJob, name='update_job'),
    path('jobs/<str:pk>/delete/', views.deleteJob, name='delete_job'),
    path('stats/<str:topic>/', views.getTopicStats, name='get_topic_stats'),

    path('jobs/<str:pk>/apply/', views.applyToJob, name='apply_to_job'),
    path('jobs/<str:pk>/favorite/', views.favoriteJob, name='favorite_job'),
    path('me/jobs/applied/', views.getCurrentUserAppliedJobs, name='current_user_applied_jobs'),
    path('me/jobs/favorites/', views.getCurrentUserFavoriteJobs, name='current_user_favorite_jobs'),
    path('jobs/<str:pk>/check/', views.isApplied, name='is_applied_to_job'),
    path('me/jobs/', views.getCurrentUserJobs, name='current_user_jobs'),
    path('job/<str:pk>/candidates/', views.getCandidatesApplied, name='get_candidates_applied'),


    path('remotejobs/', views.getRemoteJobs, name='get_remote_jobs'),
    path('hottestjobs/', views.getHottestJobs, name='get_hottest_jobs'),
    path('newestjobs/', views.getNewestJobs, name='get_newest_jobs'),
    path('fresherjobs/', views.getFresherJobs, name='get_fresher_jobs'),
]