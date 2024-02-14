from django.urls import path
from . import views
urlpatterns = [
    path('group/<str:groupname>/', views.create_group, name = 'create-group'),
]