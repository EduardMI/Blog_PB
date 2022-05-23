# from .models import News
# from django.forms import ModelForm, TextInput, Textarea, ImageField
#
#
# class NewsForm(ModelForm):
#     class Meta:
#         model = News
#         fields = ['author','title', 'anons', 'full_text', 'image']
#
#         widgets = {
#             'title': TextInput(attrs={
#                 'class': 'form-control',
#                 'placerholder': 'Название статьи'
#             }),
#             'anons': Textarea(attrs={
#                 'class': 'form-control',
#                 'placerholder': 'Анонс'
#             }),
#             'full_text': Textarea(attrs={
#                 'class': 'form-control',
#                 'placerholder': 'Текст статьи'
#             }),
#         }

from django.forms import ModelForm

from news.models import News


class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ('title', 'anons', 'full_text', 'author', 'image')

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'