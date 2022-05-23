from django.urls import path
from .views import LoginUserView, LogoutUserView, RegisterUserView, VerifyView, ProfileEditView, UserDetailView, \
    UserChangePassword
from django.conf.urls import include, url

app_name = 'authapp'

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('edit/<int:pk>/', ProfileEditView.as_view(), name='edit'),
    path('verify/<email>/<activation_key>', VerifyView.as_view(), name='verify'),
    path('profile/<int:pk>', UserDetailView.as_view(), name='profile'),
    path('change-password/', UserChangePassword.as_view(), name='change_pass'),
]
