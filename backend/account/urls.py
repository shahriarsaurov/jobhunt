from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('me/', views.currentUser, name='current_user'),
    path('me/update/', views.updateUser, name='update_user'),
    path('upload/docs/', views.updateUser, name='update_docs'),
    path('all/', views.getAllUsers, name='get_all_users'),
    #    path('upload/resume/', views.uploadResume, name='upload_resume'),
]