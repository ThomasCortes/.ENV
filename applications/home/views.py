from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class indexviews(TemplateView):
    template_name = 'index.html'
    

def home(request):
    return render(request, "index.html")


