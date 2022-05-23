from django.forms import ModelForm
from adminapp.forms import add_class_html
from articleapp.models import Article


class ArticleForm(ModelForm):
    """
    класс - Форма для статей
    """
    class Meta:
        """
        класс - Мета
        """
        model = Article
        fields = ('title', 'category', 'content', 'image')

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ArticleApprove(ModelForm):
    """
    класс - Модерация статей
    """
    class Meta:
        """
        класс - Мета
        """
        model = Article
        exclude = ['uid', 'title', 'content', 'author', 'category',
                   'created', 'updated', 'image', 'status', 'liked', 'objects']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)
