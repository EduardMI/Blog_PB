from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views import about, help

urlpatterns = [
    path('admin/', admin.site.urls),
    path('_admin/', include('adminapp.urls', namespace='_admin')),
    path('temp/', include('mainapp.urls')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('news/', include('news.urls', namespace='news')),
    path('', include('articleapp.urls', namespace='article')),
    path('', include('social_django.urls', namespace='social')),
    path('', include('searchapp.urls', namespace='search')),
    path('notification/', include('notificationapp.urls', namespace='notify')),
    path('about/', about, name='about'),
    path('help/', help, name='help'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
