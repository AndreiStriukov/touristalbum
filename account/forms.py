from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.utils.translation import gettext_lazy as _

from django.forms import SelectDateWidget, ClearableFileInput, ImageField
import datetime
from django.contrib.auth import authenticate

from .models import *

year = datetime.date.today().year

MONTHS_CHOICES = {
    "1": _("January"),
    "2": _("February"),
    "3": _("March"),
    "4": _("April"),
    "5": _("May"),
    "6": _("June"),
    "7": _("July"),
    "8": _("August"),
    "9": _("September"),
    "10": _("October"),
    "11": _("November"),
    "12": _("December"),
}


class LoginUserForm(forms.ModelForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form_email'}))
    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form_password'}))

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
                raise forms.ValidationError(_("Authorization error"))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='',
                               widget=forms.TextInput(attrs={
                                   'placeholder': _('Username'),
                                   'class': 'form_username'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form_email'}))
    password1 = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form_password'}))
    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={'placeholder': _('Confirm password'), 'class': 'form_password'}))

    class Meta:
        model = AdvUser
        fields = ('email', 'username', 'password1', 'password2', 'user_lang', 'send_messages')
        labels = {'user_lang': _('Language'), 'send_messages': _('Send messages')}


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = AdvUser
        fields = ('first_name', 'last_name', 'birthday', 'user_lang', 'send_messages', 'hide_email')
        labels = {'first_name': _('First name'), 'last_name': _('Last name'), 'birthday': _('Birthday'),
                  'user_lang': _('Language'), 'send_messages': _('Send messages'), 'hide_email': _('Do not display email')}
        widgets = {
            'birthday': SelectDateWidget(years=range(year, year - 100, -1), months = MONTHS_CHOICES,
                                         empty_label=(_('year'), _('month'), _('day')))
        }


class MyClearableFileInput(ClearableFileInput):
    initial_text = _('Current')
    input_text = _('Select image')
    clear_checkbox_label = _('Clear')
    selected_filename = _('File not selected')
    template_name = "account/widgets/clearable_file_input.html"

class UpdateProfileForm(forms.ModelForm):
    avatar = ImageField(label=_('Avatar'), required = False, widget=MyClearableFileInput)
    class Meta:
        model = AdvUser
        fields = ('avatar',)
