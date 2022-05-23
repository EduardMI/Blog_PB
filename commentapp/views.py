from django.urls import reverse_lazy
from django.contrib import messages


class SuccessMessage:
    """
    класс - Оповещение
    """
    def success_msg(self):
        """
        :return:
        """
        return False

    def form_valid(self, form):
        """
        :param form:
        :return:
        """
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        """
        :return:
        """
        return '%s?id=%s' % (self.success_url, self.object.id)


class CommentView(SuccessMessage):
    """
    класс - CommentView
    """
    success_msg = 'Комментарий успешно создан.'

    def get_success_url(self, **kwargs):
        """
        :param self:
        :param kwargs:
        :return:
        """
        return reverse_lazy('articleapp:detail',
                            kwargs={'pk': self.get_object().uid})

    def post(self, request, *args, **kwargs):
        """
        :param self:
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        :param self:
        :param form:
        :return:
        """
        self.object = form.save(commit=False)
        self.object.comment_article = self.get_object()
        self.object.comment_author = self.request.user
        self.object.save()
        return super().form_valid(form)
