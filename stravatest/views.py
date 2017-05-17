# -*- coding: utf-8 -*-

# trips/views.py

from datetime import datetime
from django.shortcuts import render
from django.views.generic import TemplateView

#hello world
def hello_world(request):
    return render(request, 'hello_world.html', {
        'current_time': str(datetime.now()),
    })


class HomeView(TemplateView):
    template_name = "home.html"
