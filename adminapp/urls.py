from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.MainView.as_view(), name='main_admin'),
    path('users/', adminapp.UserListView.as_view(), name='users'),
    path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('users/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),

    path('categories/create/', adminapp.CategoryCreateView.as_view(), name='category_create'),
    path('categories/', adminapp.CategoryListView.as_view(), name='categories'),
    path('categories/update/<int:pk>/', adminapp.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),

    path('articles/create/', adminapp.ArticleCreateView.as_view(), name='article_create'),
    path('articles/', adminapp.ArticlesListView.as_view(), name='articles'),
    path('articles/update/<uuid:pk>/', adminapp.ArticleUpdateView.as_view(), name='article_update'),
    path('articles/delete/<uuid:pk>/', adminapp.ArticleDeleteView.as_view(), name='article_delete'),

    path('comments/create/', adminapp.CommentCreateView.as_view(), name='comment_create'),
    path('comments/', adminapp.CommnetsListView.as_view(), name='comments'),
    path('comments/update/<int:pk>/', adminapp.CommentUpdateView.as_view(), name='comment_update'),
    path('comments/delete/<int:pk>/', adminapp.CommentDeleteView.as_view(), name='comment_delete'),

    path('news/', adminapp.NewsListView.as_view(), name='news'),
    path('news/create/', adminapp.NewsCreateView.as_view(), name='news_create'),
    path('news/update/<int:pk>/', adminapp.NewsUpdateView.as_view(), name='news_update'),
    path('news/delete/<int:pk>/', adminapp.NewsDeleteView.as_view(), name='news_delete'),

    path('moder/', adminapp.ModerListView.as_view(), name='moder'),
    path('moder/article/<uuid:pk>/', adminapp.ApproveArticle.as_view(), name='approve_article'),
    path('moder/news/<int:pk>/', adminapp.ApproveNews.as_view(), name='approve_news'),
    path('moder/notify/delete/<int:pk>/', adminapp.NotifyDeleteView.as_view(), name='notify_delete'),
    path('moder/block/<int:pk>', adminapp.UserBlock.as_view(), name='user_block'),
]
