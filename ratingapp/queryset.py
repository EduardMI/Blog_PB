from django.db.models import F
# from django.db.models import Subquery, OuterRef
from django.db.models import Value as V,Q
# from django.db.models import Value as Q
from django.db.models.functions import Coalesce


def add_rating(queryset):
    """ Добавление рейтинга в queryset"""

    # context['object_list'] = context['object_list']\
    #     .annotate(rating=Subquery(
    #     ArticleRating.objects.annotate(rating=(F('likes')+F('comments')))
    #         .filter(article_id=OuterRef('uid')).values('rating')[:1])
    # )
    return queryset.select_related('articlerating').\
        annotate(rating=Coalesce(F('articlerating__likes')+F('articlerating__comments'), V(0)))