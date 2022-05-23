from django.forms import ModelForm, Textarea
from .models import Comments


class CommentsForm(ModelForm):
    """
    класс - форма для комментария
    """

    class Meta:
        """
        класс - Мета
        """
        model = Comments
        fields = ('comment_text',)

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['comment_text'].widget = Textarea(attrs={'rows': 4, 'cols': 80})
