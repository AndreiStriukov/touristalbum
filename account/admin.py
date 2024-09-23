from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserChangeForm


class LangAdmin(admin.ModelAdmin):
    list_display = ('lang_code', 'lang_name')


class AdvUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = AdvUser


class AdvUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = AdvUser
        fields = ('email',)

        def save(self, commit=True):
            # Save the provided password in hashed format
            user = super(UserCreationForm, self).save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user


class AdvUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = AdvUserCreationForm
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'email_verify', 'send_messages',
                    'is_admin', 'is_active')
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'avatar', 'birthday',
                           'send_messages', 'is_admin', 'is_active', 'email_verify')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',
                       'user_lang', 'birthday', 'send_messages', 'is_admin',
                       'is_active', 'email_verify')}
         ),
    )

    filter_horizontal = ()

    list_filter = ()


admin.site.register(AdvUser, AdvUserAdmin)

admin.site.register(Lang, LangAdmin)
