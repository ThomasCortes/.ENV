from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class indexviews(TemplateView):
    template_name = 'index.html'

def home(request):
    return render(request, "index.html")

class MainViews(TemplateView):
    template_name = 'main.html'

def home(request):
    return render(request, "main.html")


