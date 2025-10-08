from django.shortcuts import render
from .models import Model


class HomeView:
    def home(request):
        return render(request, 'home.html')

