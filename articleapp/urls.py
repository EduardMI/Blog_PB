from django.urls import path
from articleapp.views import IndexView, ArticleDetailView, \
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView, like_art, \
    CategoryArticleView, ArticleListView, ArticlePublished


app_name = 'articleapp'

urlpatterns = [
    path('', IndexView.as_view(), name='main'),
    path('index/', IndexView.as_view(), name='main'),
    path('article/new/', ArticleCreateView.as_view(), name='add'),
    path('article/list/', ArticleListView.as_view(), name='list'),
    path('article/<uuid:pk>/', ArticleDetailView.as_view(), name='detail'),
    path('article/<uuid:pk>/edit/', ArticleUpdateView.as_view(), name='edit'),
    path('article/<uuid:pk>/delete/', ArticleDeleteView.as_view(),
         name='delete'),
    path('article/<uuid:pk>/like/', like_art, name='like-art'),
    path('article/category/<int:pk>', CategoryArticleView.as_view(), name='article_category'),
    path('article/<uuid:pk>/published/', ArticlePublished.as_view(), name='public'),
]
