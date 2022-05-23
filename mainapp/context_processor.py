# TODO разобраться можно ли наследовать существующий контекстный процессор для работы с меню.
from articleapp.models import Category


def menu_category_context(request):

    categories = Category.objects.all().filter(is_active=True)

    return {
        'categories': categories
        }


