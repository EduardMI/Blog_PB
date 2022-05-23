from django.http import HttpResponseRedirect
from django.views.generic import ListView, DeleteView

from .models import NotifyUser
from .mixins import UserAccessNotifyMixin


class NotificationListVew(UserAccessNotifyMixin, ListView):
    model = NotifyUser
    context_object_name = 'notify'
    template_name = 'notificationapp/notifyuser_list.html'
    paginate_by = 20

    def get_queryset(self):
        return NotifyUser.objects.filter(user_to=self.kwargs['pk'])


class NotificationIsReadVew(UserAccessNotifyMixin, DeleteView):
    model = NotifyUser

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    # def delete(self, request, *args, **kwargs):
    #     """
    #     Call the delete() method on the fetched object and then redirect to the
    #     success URL.
    #     """
    #     self.object = self.get_object()
    #     success_url = self.get_success_url()
    #     self.object.delete()
    #     return HttpResponseRedirect(success_url)
