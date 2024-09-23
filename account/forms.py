from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.forms import SelectDateWidget, ClearableFileInput, ImageField
import datetime
from django.contrib.auth import authenticate

from .models import *

year = datetime.date.today().year

RU_MONTHS_CHOICES = {
    "1": "Январь",
    "2": "Февраль",
    "3": "Март",
    "4": "Апрель",
    "5": "Май",
    "6": "Июнь",
    "7": "Июль",
    "8": "Август",
    "9": "Сентябрь",
    "10": "Октябрь",
    "11": "Ноябрь",
    "12": "Декабрь",
}


class LoginUserForm(forms.ModelForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form_email'}))
    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form_password'}))

    class Meta:
        model = AdvUser
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            self.user_cache = authenticate(
                email=email,
                password=password,
            )

            if self.user_cache is None:
                raise forms.ValidationError("Ошибка авторизации")


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='',
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Логин',
                                   'class': 'form_username'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form_email'}))
    password1 = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form_password'}))
    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля', 'class': 'form_password'}))

    class Meta:
        model = AdvUser
        fields = ('email', 'username', 'password1', 'password2', 'user_lang', 'send_messages')
        labels = {'user_lang': 'Язык', 'send_messages': 'Отправлять сообщения'}


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = AdvUser
        fields = ('first_name', 'last_name', 'birthday', 'user_lang', 'send_messages', 'hide_email')
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'birthday': 'День рождения',
                  'user_lang': 'Язык', 'send_messages': 'Отправлять сообщения', 'hide_email': 'Не отображать Email'}
        widgets = {
            'birthday': SelectDateWidget(years=range(year, year - 100, -1), months = RU_MONTHS_CHOICES,
                                         empty_label=(u'год', u'месяц', u'число'))
        }


class MyClearableFileInput(ClearableFileInput):
    initial_text = 'Текущий'
    input_text = 'Выберите изображение'
    clear_checkbox_label = 'Очистить'
    template_name = "account/widgets/clearable_file_input.html"

class UpdateProfileForm(forms.ModelForm):
    avatar = ImageField(label='Аватар', required = False, widget=MyClearableFileInput)
    class Meta:
        model = AdvUser
        fields = ('avatar',)
