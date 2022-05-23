from django.urls import path
from searchapp.views import search


app_name = 'searchapp'

urlpatterns = [
    path('search', search, name='search'),
]
