from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


from authapp.models import HabrUser, HabrProfile
from articleapp.models import Category, Article
from commentapp.models import Comments
from news.models import News

CHECK_LIST = ['is_active', 'is_delete', 'is_staff', 'is_deleted',
              'comment_moderation', 'approve']


def add_class_html(fields):
    for field_name, field in fields.items():
        if field_name in CHECK_LIST:
            field.widget.attrs['class'] = 'form-chek'
            field.help_text = ''
            continue
        else:
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = HabrUser
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'role', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)


class UserCreateForm(UserCreationForm):
    class Meta:
        model = HabrUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1',
                  'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = HabrProfile
        fields = ('tagline', 'gender', 'birthday', 'zone')

    birthday = forms.DateField(label='Дата рождения',
                               required=True,
                               widget=forms.SelectDateWidget(years=range(1950, 2010)),
                               )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'category', 'content', 'author',
                  'image', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)


class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        # fields = ('title', 'category', 'content', 'author', 'image', 'status')
        exclude = ['uid', 'liked', 'publication_date', 'approve']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['comment_moderation', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'anons', 'full_text', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)


class NewsUpdateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'anons', 'full_text', 'author','image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)


class ApproveArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ()


class ApproveNewsForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ()
