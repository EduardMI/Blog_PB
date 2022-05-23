from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404

from authapp.models import HabrUser


class UserAccessNotifyMixin(UserPassesTestMixin):
    """ Предоставляет право доступа пользователю к уведомлениям """

    def test_func(self):
        user = self.request.user
        profile_user = get_object_or_404(HabrUser, pk=self.kwargs['pk'])
        if user.is_authenticated:
            if user == profile_user or user.is_superuser:
                return True

    def handle_no_permission(self):
        return redirect('/')
