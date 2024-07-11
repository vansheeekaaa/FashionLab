from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('submit_design/', views.submit_design, name='submit_design'),
    path('vote/<int:design_id>/', views.vote, name='vote'),
    path('lab/', views.lab, name='lab'),
    path('win/', views.win, name='win'),
    path('create_avatar/', views.create_avatar, name='create_avatar'),  # This line is important
    path('my-closet/', views.my_closet, name='my_closet'),
]
