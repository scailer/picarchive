from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views import generic
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', generic.TemplateView.as_view(template_name='main.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('apps.account.urls')),
    url(r'^picture/', include('apps.picture.urls')),
    url(r'^notice/', include('apps.notice.urls')),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
