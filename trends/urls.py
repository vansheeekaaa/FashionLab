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
]
