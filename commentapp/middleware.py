from django.utils.deprecation import MiddlewareMixin
import threading

_local_storage = threading.local()


class RequestMiddlewareUser(MiddlewareMixin):
    """
    класс - MiddlewareUser
    """

    def process_request(self, request):
        """
        :param request:
        :return:
        """
        _local_storage.request = request


def get_current_request():
    """
    :return:
    """
    return getattr(_local_storage, 'request', None)


def get_current_user():
    """
    :return:
    """
    request = get_current_request()
    if request is None:
        return None
    return getattr(request, 'user', None)
