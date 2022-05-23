from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class UserIsAdminMixin(UserPassesTestMixin):
    """ Предоставляет право доступа пользователю у которого роль Администратор """

    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return user.role == 'A' or user.is_superuser

    def handle_no_permission(self):
        return redirect('/')


class UserIsPersonalMixin(UserPassesTestMixin):
    """ Предоставляет право доступа пользователю у которого роль Администратор или Модератор"""
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return user.role != 'U' or user.is_superuser

    def handle_no_permission(self):
        return redirect('/')
