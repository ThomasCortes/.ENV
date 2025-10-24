from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexviews.as_view(), name='home'),
]