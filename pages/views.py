# Тест комита
from django.shortcuts import render


def about(request):
    template_name = 'pages/about.html'
    return render(request, template_name)
