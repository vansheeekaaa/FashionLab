from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('vote/', views.vote_view, name='vote_view'),    
    path('submit_design/', views.submit_design, name='submit_design'),
    path('lab/', views.lab, name='lab'),
    path('win/', views.win, name='win'),
    path('my-closet/', views.my_closet, name='my_closet'),
    path('success/', views.success, name='success'),
    path('design/<int:design_id>/upvote/', views.upvote_design, name='upvote_design'), 
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'), 
    path('login/', views.user_login, name='login'),  # Add this line
]

