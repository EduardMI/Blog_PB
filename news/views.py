from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from adminapp.mixins import UserIsPersonalMixin
from .models import News
from .forms import NewsForm
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView


#
# def news_main(request):
#     news = News.objects.order_by('-date')
#     return render(request, "news/news_main.html", {'news': news})

# def create_news(request):
#     error = ''
#     if request.method == "POST":
#         form = NewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('news:main')
#         else:
#             error = "Ошибка вводда данных"
#     form_news = NewsForm()
#     data = {
#         'form': form_news,
#         'error': error
#     }
#     return render(request, "news/create_news.html", data)


class NewsListView(ListView):
    model = News
    queryset = News.objects.filter(status__icontains='PB').order_by('-date')
    template_name = 'news/news_main.html'
    context_object_name = 'news'


class NewsCreateView(UserIsPersonalMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'adminapp/news/news_create.html'
    success_url = reverse_lazy('news:main')


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail_news.html'
    context_object_name = 'detail_view'


class NewsUpdateView(UserIsPersonalMixin, UpdateView):
    model = News
    template_name = 'news/create_news.html'
    form_class = NewsForm
    reverse_lazy('news:main')


class NewsDeleteView(UserIsPersonalMixin, DeleteView):
    model = News
    template_name = 'news/delete_news.html'
    success_url = reverse_lazy('news:main')
