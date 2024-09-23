
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# def get_redirect_if_exists(request):
#     redirect_u = None
#     if request.GET:
#         if request.GET.get("next"):
#             redirect_u = str(request.GET.get("next"))
#     return redirect_u


def send_email_for_verify(request, user):
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # первичный ключ пользователя, закодированный в base64.
        'token': token_generator.make_token(user),  # токен, используемый для проверки действительности ссылки
    }

    message = render_to_string(
        'account/registration/verify_email.html',
        context=context,
    )

    email = EmailMessage(
        'Veryfi email',
        message,
        to=[user.email],
    )
    email.send()

