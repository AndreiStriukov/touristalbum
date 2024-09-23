from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.contrib import messages, auth
from django.http import JsonResponse

from .forms import *
from .utils import *
from .models import *


class AccountView(LoginRequiredMixin, DetailView):

    """
    Представление для просмотра профиля
    """
    model = AdvUser
    context_object_name = 'account_detail'
    pk_url_kwarg = 'user_id'
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u_email = self.object.email
        account = AdvUser.objects.get(email=u_email)
        if account.first_name:
            user_name = str(account.first_name) + ' ' + str(account.last_name)
        else:
            user_name = str(account.username)
        context['title'] = 'Альбом туриста. Профиль пользователя ' + user_name
        return context


class LoginView(View):

    def post(self, request):
        user = request.user

        if not user.is_authenticated:
            email = request.POST['email']
            password = request.POST['password']

            if email and password:
                user = authenticate(email=email, password=password )
                if user:
                    if user.email_verify:
                        login(request, user)
                        return JsonResponse(
                            data={'status': 201},
                            status=200
                        )
                    else:
                        send_email_for_verify(request, user)
                        return JsonResponse(
                            data={
                                'status': 202,
                                'error': 'Регистрация не завершена, т.к. нет подтверждения! <br>'
                                         + '<i class="fa fa-envelope-open-o" aria-hidden="true"></i> '
                                         + 'Пожалуйста проверьте свою почту'
                                         + 'чтобы продолжить регистрацию.'
                            },
                            status=200
                        )
                else:
                    return JsonResponse(
                        data={
                            'status': 203,
                            'error': 'Не удается идентифицировать пользователя. <br>'
                                     + 'Проверьте вводимые email и пароль'
                        },
                        status=200
                    )
            else:
                return JsonResponse(
                    data={
                        'status': 204,
                        'error': 'Не задан пароль или логин!'
                    },
                    status=200
                )
        else:
            return JsonResponse(
                data={
                    'status': 400,
                    'error': 'Пользователь уже авторизован'
                },
                status=200
            )


@login_required
def logout_view(request):
    logout(request)
    return redirect("index")


class RegisterView(CreateView):
    template_name = 'account/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('confirm_email')

    def form_valid(self, form):
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        send_email_for_verify(self.request, user)  # в утилитах
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создайте профиль. Присоединяйтесь к АЛЬБОМ Туриста'
        context['head'] = 'Добро пожаловать! Присоединяйтесь'
        context['button'] = 'Создать профиль'
        return context


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()  # нужно сохранить пользователя
            login(request, user)
            return redirect('profile', user_id=user.pk)
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = AdvUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                AdvUser.DoesNotExist, ValidationError):
            user = None
        return user


def edit_account(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user_pk = request.user.pk
    account = AdvUser.objects.get(pk=user_pk)

    context = {
        'title': request.user.username + '. Изменение профиля. Альбом туриста',
        'head': 'Изменение профиля',
        'button': 'Изменить',
        'top_head': request.user.username,
    }

    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST, request.FILES,
                                   instance=request.user, initial={'avatar': account.avatar})
        if u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль был успешно обновлен.')
            return redirect('profile', user_id=user_pk)
    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = UpdateProfileForm(initial={'avatar': account.avatar})

    context['u_form'] = u_form
    context['p_form'] = p_form

    return render(request, "account/edit_profile.html", context)
