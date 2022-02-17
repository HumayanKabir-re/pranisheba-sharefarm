from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.conf.urls import url, re_path
from django.conf.urls import include as rest_include
from core.urls import core_auth_urlpatterns
from sharedfarm.urls import sharedfarm_api_urlpatterns, sharedfarm_blog_api_urlpatterns
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.views.i18n import JavaScriptCatalog

admin.autodiscover()
schema_view = get_schema_view(
    openapi.Info(
        title="Joutho Khamar Rest API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = i18n_patterns(
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
)

# urlpatterns = [
#
# ]

api_v1_urlpatterns = [
    path('auth/', include((core_auth_urlpatterns, 'users'), namespace='users')),
    path('sharedfarm/', include((sharedfarm_api_urlpatterns, 'sharedfarm'), namespace='sharedfarm')),
    path('blog/', include((sharedfarm_blog_api_urlpatterns, 'blog'), namespace='blog')),
    # url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('content/', include('content.urls')),
    # path('subscription/', include('subscription.urls')),
    # path('transection/', include('payment.urls')),

]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^api/v1/', include((api_v1_urlpatterns, 'v1'), namespace='v1')),
    re_path(r'^accounts/', include('core.urls', )),
    path("", include("cms.urls")),
    re_path(r'^sharedfarm/', include('sharedfarm.urls', )),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
