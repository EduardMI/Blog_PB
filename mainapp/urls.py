from django.urls import path, include

from mainapp.views import main

urlpatterns = [
    path('', main, name='main'),
    path('index/', main),
]

