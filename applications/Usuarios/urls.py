from django.urls import path
from .views import RegisterView,LoginView
from applications.home.urls import urlpatterns as home_urls

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

] + home_urls
    
