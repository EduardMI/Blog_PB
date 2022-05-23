from django.urls import path
from . import views
app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='main'),
    path('create_news', views.NewsCreateView.as_view(), name='create_news'),
    path('<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),
    path('<int:pk>/update', views.NewsUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete', views.NewsDeleteView.as_view(), name='news_delete')
]