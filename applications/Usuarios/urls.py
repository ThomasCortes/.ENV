from django.urls import path
from .views import RegisterView,LoginView,PasswordView
from applications.home.urls import urlpatterns as home_urls
#nuevas rls
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('recuperar/', PasswordView.as_view(), name='recuperar'),
#NUEVOS PATH
    path('recover/', views.send_verification_code, name='send_verification_code'),
    path('verificar/', views.verify_code, name='verify_code'),
    path('cambiar/', views.change_password, name='change_password'),

] + home_urls
    
