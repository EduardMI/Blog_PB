from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404

from articleapp.models import Article


class UserIsNoBlockMixin(UserPassesTestMixin):
    """ Предоставляет право доступа пользователю который не заблокирован """

    def test_func(self):
        user = self.request.user
        author = get_object_or_404(Article, pk=self.kwargs['pk']).author
        if user.is_authenticated:
            if user == author:
                return user.check_block() is False

    def handle_no_permission(self):
        return redirect('/')
