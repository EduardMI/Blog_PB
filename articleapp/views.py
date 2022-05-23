from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, \
    DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin

from articleapp.forms import ArticleForm, ArticleApprove
from articleapp.models import Article, Like, Category
from commentapp.forms import CommentsForm
from commentapp.views import CommentView
from mainapp.views import main
from ratingapp.models import ArticleRating
from ratingapp.queryset import add_rating
from .mixins import UserIsNoBlockMixin

# Отображение содержимого из модели Article
class IndexView(ListView):
    """
    класс - Index
    """
    queryset = add_rating(Article.objects.filter(approve=True))
    paginate_by = 4
    template_name = 'mainapp/index.html'
    ordering = ('-publication_date', '-created')


# Отображение списка статей
class ArticleListView(ListView):
    """
    класс - ArticleList
    """
    model = Article
    paginate_by = 5
    template_name = 'articles_list.html'

    def get_queryset(self):
        """
        :return:
        """
        return Article.objects.filter(author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['object_list'] = add_rating(context['object_list'])

        return context


# Отображение содержимого
class ArticleDetailView(CommentView, FormMixin, DetailView):
    """
    класс - ArticleDetail
    """
    model = Article
    form_class = CommentsForm
    second_form_class = ArticleApprove
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.object.comments)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=self.object)

        try:
            rating = get_object_or_404(ArticleRating, article=self.object)
            context['rating'] = rating.value()
        except Exception:
            # TODO обработать конкретное исключение
            context['rating'] = 0

        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    класс - ArticleCreate
    """
    model = Article
    template_name = 'article_new.html'
    form_class = ArticleForm

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        form = self.get_form()
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            self.object = article.save()
            return redirect('auth:profile', request.user.pk)

        return self.form_invalid(form)


class ArticleUpdateView(UserIsNoBlockMixin, UpdateView):
    """
    класс - ArticleUpdate
    """
    model = Article
    template_name = 'article_edit.html'
    fields = ['title', 'category', 'content', 'image']


class ArticleDeleteView(UserIsNoBlockMixin, DeleteView):
    """
    класс - ArticleDelete
    """
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy(main)


class ArticlePublished(UserIsNoBlockMixin, DeleteView):
    """
    класс - Публикация статьи
    """
    model = Article

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def delete(self, request, *args, **kwargs):
        """  """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.status = 'PB'
        self.object.save()
        return HttpResponseRedirect(success_url)


def like_art(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    user = request.user
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        article_obj = Article.objects.get(pk=article_id)

        if user in article_obj.liked.all():
            article_obj.liked.remove(user)
        else:
            article_obj.liked.add(user)
        like, created = Like.objects.get_or_create(user=user,
                                                   article_id=article_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Dislike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

            article_obj.save()
            like.save()

        data = {
            'value': like.value,
            'likes': article_obj.liked.all().count()
        }
        return JsonResponse(data, safe=False)

    return redirect('article:detail', pk=pk)


class CategoryArticleView(ListView):
    """
    класс - Сортировка статей по категориям
    """
    model = Article
    template_name = 'category.html'
    paginate_by = 6

    def get_queryset(self):
        """
        :return:
        """
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])

        queryset = Article.objects.filter(category=self.category)\
            .filter(status='PB', approve=True)
        queryset = add_rating(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        context = super(CategoryArticleView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context
