from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils import timezone

from commentapp.models import Comments
from news.models import News
from .forms import UserUpdateForm, UserCreateForm, ProfileUpdateForm, CategoryCreateForm, ArticleCreateForm, \
    ArticleUpdateForm, CommentCreateForm, CommentUpdateForm, NewsCreateForm, NewsUpdateForm, \
    ApproveArticleForm, ApproveNewsForm
from .mixins import UserIsPersonalMixin, UserIsAdminMixin
from articleapp.models import Category, Article
from authapp.models import HabrUser
from .models import NotifyComment


# главная страница админки
class MainView(UserIsPersonalMixin, TemplateView):
    template_name = 'adminapp/main_admin.html'


class UserListView(UserIsPersonalMixin, ListView):
    model = HabrUser
    template_name = 'adminapp/users/users.html'
    context_object_name = 'objects'
    paginate_by = 10
    ordering = ['role']


class UserCreateView(UserIsAdminMixin, CreateView):
    model = HabrUser
    form_class = UserCreateForm
    template_name = 'adminapp/users/user_create.html'
    success_url = reverse_lazy('_admin:users')


class UserUpdateView(UserIsAdminMixin, UpdateView):
    model = HabrUser
    template_name = 'adminapp/users/user_update.html'
    success_url = reverse_lazy('_admin:users')
    form_class = UserUpdateForm
    second_form_class = ProfileUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.object)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=self.object.habrprofile)
        context['avatar'] = self.object.avatar
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form2 = self.second_form_class(request.POST, instance=self.object.habrprofile)
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid() and form2.is_valid():
            form2.save()
            return super().post(request, *args, **kwargs)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2))


class UserDeleteView(UserIsPersonalMixin, DeleteView):
    model = HabrUser
    template_name = 'adminapp/users/user_delete.html'
    success_url = reverse_lazy('_admin:users')
    context_object_name = 'user_to_delete'


# контроллеры для категорий
class CategoryListView(UserIsPersonalMixin, ListView):
    model = Category
    template_name = 'adminapp/categories/categories.html'
    context_object_name = 'objects'
    paginate_by = 10


class CategoryCreateView(UserIsAdminMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'adminapp/categories/category_create.html'
    success_url = reverse_lazy('_admin:categories')


class CategoryUpdateView(UserIsAdminMixin, UpdateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'adminapp/categories/category_update.html'
    success_url = reverse_lazy('_admin:categories')


class CategoryDeleteView(UserIsAdminMixin, DeleteView):
    model = Category
    template_name = 'adminapp/categories/category_delete.html'
    success_url = reverse_lazy('_admin:categories')
    context_object_name = 'category_to_delete'


# контроллеры для статей
class ArticlesListView(UserIsPersonalMixin, ListView):
    model = Article
    template_name = 'adminapp/articles/articles.html'
    context_object_name = 'objects'
    paginate_by = 10


class ArticleCreateView(UserIsPersonalMixin, CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'adminapp/articles/article_create.html'
    success_url = reverse_lazy('_admin:articles')


class ArticleUpdateView(UserIsAdminMixin, UpdateView):
    model = Article
    form_class = ArticleUpdateForm
    template_name = 'adminapp/articles/article_update.html'
    success_url = reverse_lazy('_admin:articles')


class ArticleDeleteView(UserIsPersonalMixin, DeleteView):
    model = Article
    template_name = 'adminapp/articles/article_delete.html'
    context_object_name = 'article_to_delete'
    success_url = reverse_lazy('_admin:articles')


# контроллеры для комментов
class CommnetsListView(UserIsPersonalMixin, ListView):
    model = Comments
    template_name = 'adminapp/comments/comments.html'
    context_object_name = 'objects'
    paginate_by = 10


class CommentCreateView(UserIsPersonalMixin, CreateView):
    model = Comments
    form_class = CommentCreateForm
    template_name = 'adminapp/comments/comment_create.html'
    success_url = reverse_lazy('_admin:comments')


class CommentUpdateView(UserIsAdminMixin, UpdateView):
    model = Comments
    form_class = CommentUpdateForm
    template_name = 'adminapp/comments/comment_update.html'
    success_url = reverse_lazy('_admin:comments')


class CommentDeleteView(UserIsPersonalMixin, DeleteView):
    model = Comments
    template_name = 'adminapp/comment/comment_delete.html'
    context_object_name = 'comment_to_delete'
    # success_url = reverse_lazy('_admin:comments')

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

# контроллеры для новостей
class NewsListView(UserIsPersonalMixin, ListView):
    model = News
    template_name = 'adminapp/news/news.html'
    context_object_name = 'objects'
    paginate_by = 10


class NewsCreateView(UserIsPersonalMixin, CreateView):
    model = News
    form_class = NewsCreateForm
    template_name = 'adminapp/news/news_create.html'
    success_url = reverse_lazy('_admin:news')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            self.object = form.save()
            return super().form_valid(form)


class NewsUpdateView(UserIsPersonalMixin, UpdateView):
    model = News
    form_class = NewsUpdateForm
    template_name = 'adminapp/news/news_update.html'
    success_url = reverse_lazy('_admin:news')


class NewsDeleteView(UserIsPersonalMixin, DeleteView):
    model = News
    template_name = 'adminapp/news/news_delete.html'
    context_object_name = 'news_to_delete'
    success_url = reverse_lazy('_admin:news')


# контролеры для модерации
class ModerListView(UserIsPersonalMixin, TemplateView):
    template_name = 'adminapp/moder/moder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all().filter(approve=False, status='PB')
        context['notifications'] = NotifyComment.objects.all().filter(is_read=False)
        context['news'] = News.objects.all().filter(status='DF')
        return context


class ApproveArticle(UserIsPersonalMixin, UpdateView):
    model = Article
    template_name = 'adminapp/moder/article_approve.html'
    success_url = reverse_lazy('_admin:moder')
    form_class = ApproveArticleForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.approve = True
        self.object.publication_date = timezone.now()
        self.object.save(update_fields=['approve', 'publication_date'])
        # self.object.save()
        return super().post(request, *args, **kwargs)


class ApproveNews(UserIsPersonalMixin, UpdateView):
    model = News
    template_name = 'adminapp/moder/news_approve.html'
    success_url = reverse_lazy('_admin:moder')
    form_class = ApproveNewsForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = 'PB'
        self.object.date = timezone.now()
        self.object.save()
        return super().post(request, *args, **kwargs)


class NotifyDeleteView(UserIsPersonalMixin, DeleteView):
    model = NotifyComment
    success_url = reverse_lazy('_admin:moder')


class UserBlock(UserIsPersonalMixin, DeleteView):
    model = HabrUser

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def delete(self, request, *args, **kwargs):
        """  """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.user_block()
        return HttpResponseRedirect(success_url)
