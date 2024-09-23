from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include, reverse_lazy
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/<int:user_id>/', views.AccountView.as_view(), name='profile'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('registration', views.RegisterView.as_view(),  name='registration'),
    path('confirm_email', TemplateView.as_view(template_name='account/registration/confirm_email.html'),
         name='confirm_email'),
    path('verify_email/<uidb64>/<token>/',
         views.EmailVerify.as_view(),
         name='verify_email',
         ),
    path(
        'invalid_verify/',
        TemplateView.as_view(template_name='accounts/registration/invalid_verify.html'),
        name='invalid_verify'
    ),
    path('password-reset/', PasswordResetView.as_view(
        template_name='account/reset/password_reset_form.html',
        email_template_name="account/reset/password_reset_email.html",
        success_url=reverse_lazy("password_reset_done")
    ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name = "account/reset/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="account/reset/password_reset_confirm.html",
         success_url=reverse_lazy("password_reset_complete")),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="account/reset/password_reset_complete.html"),
         name='password_reset_complete'),
    path('account/edit', views.edit_account, name='edit_account')
]
