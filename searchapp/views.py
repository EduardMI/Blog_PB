from django.shortcuts import render
from articleapp.models import Article
from django.db.models import Q
from commentapp.models import Comments
from authapp.models import HabrUser


def search(request):
    """
    Поиск по сайту
    :param request:
    :return:
    """
    if request.method == "POST":
        searched = request.POST['searched']
        results = Article.objects.filter(
            Q(content__icontains=searched) | Q(title__icontains=searched) |
            Q(author__username__icontains=searched) |
            Q(author__first_name__icontains=searched) |
            Q(author__last_name__icontains=searched))
        results_2 = Comments.objects.filter(
            Q(comment_author__username__icontains=searched) |
            Q(comment_author__first_name__icontains=searched) |
            Q(comment_author__last_name__icontains=searched) |
            Q(comment_text__icontains=searched))
        results_3 = HabrUser.objects.filter(
            Q(username__icontains=searched) |
            Q(first_name__icontains=searched) |
            Q(last_name__icontains=searched))
        return render(request, 'search.html',
                      {'searched': searched,
                       'results': results,
                       'results_2': results_2,
                       'results_3': results_3})
    else:
        return render(request, 'search.html',
                      {})
