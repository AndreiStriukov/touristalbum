
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from django.conf.urls.i18n import i18n_patterns

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('api-auth/', include('rest_framework.urls')),
#     path('', include('album.urls'), name='home'),
#     path('account/', include('account.urls')),
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # мультиязычность
# urlpatterns += i18n_patterns(
#     path('', include('album.urls'), name='home'),
#     path('account/', include('account.urls')),
# )


from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.urls import path

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Добавляем маршрут для i18n
    path('i18n/', include('django.conf.urls.i18n')),  # Этот маршрут нужен для работы 'set_language'
]

# Все мультиязычные маршруты
urlpatterns += i18n_patterns(
    path('', include('album.urls'), name='home'),  # Тут все мультиязычные приложения
    path('account/', include('account.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
