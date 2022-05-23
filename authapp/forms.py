from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import fields
from .models import HabrUser, HabrProfile
from django.contrib.auth import forms as auth_forms

from django.contrib.auth.forms import UserChangeForm

import random
import hashlib

CHECK_LIST = ['is_active', 'is_delete', 'is_staff', 'is_deleted']

def add_class_html(fields):
    for field_name, field in fields.items():
        if field_name in CHECK_LIST:
            field.widget.attrs['class'] = 'form-chek'
            field.help_text = ''
            continue
        else:
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = HabrUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = HabrUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1',
                  'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def save(self):
        user = super().save()

        user.is_active = False
        salt = hashlib.sha1(
            str(random.random()).encode('utf8')).hexdigest()[:6]

        user.activation_key = hashlib.sha1(
            (user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


# class UserEditForm(UserChangeForm):
#     class Meta:
#         model = HabrUser
#         # fields = ('username', 'first_name', 'password1',
#         #           'password2', 'email', 'birthday', 'avatar')
#         # fields = '__all__'
#         fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'avatar')
#
#     def __init__(self, *args, **kwargs):
#         super(UserEditForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             field.help_text = ''
#             if field_name == 'password':
#                 field.widget = forms.HiddenInput()
#
#         add_class_html(self.fields)


class UserEditForm(forms.ModelForm):
    """ Форма редактирование пользователя """
    class Meta:
        model = HabrUser
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_class_html(self.fields)


class ProfileEditForm(forms.ModelForm):
    """ Форма редактирование профиля """

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


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    class Meta:
        model = HabrUser
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        add_class_html(self.fields)
