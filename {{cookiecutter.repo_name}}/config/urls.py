from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse

def render_robots(request):
    permission = 'noindex' in settings.ROBOTS_META_TAGS and 'Disallow' or 'Allow'
    return HttpResponse('User-Agent: *\n%s: /\n' % permission, content_type='text/plain')


{% if cookiecutter.use_django_cms == 'y' -%}
sitemaps = {}

from cms.sitemaps import CMSSitemap
sitemaps['cmspages'] = CMSSitemap

    {% if cookiecutter.use_django_shop == 'y' %}
from {{ cookiecutter.app_name }}.shop.sitemap import ProductSitemap
sitemaps['products'] = ProductSitemap
    {%- endif %}

urlpatterns = [
    re_path(r'^robots\.txt$', render_robots),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    {% if cookiecutter.use_django_shop == 'y' -%}
    re_path(r'^shop/', include('shop.urls', namespace='shop')),
    {%- endif %}
]
{% else %}
urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path(settings.ADMIN_URL, admin.site.urls),
]
{%- endif %}

urlpatterns += i18n_patterns(
    # Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
    # User management
    re_path(r"^accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    {% if cookiecutter.use_django_cms == 'y' -%}
    re_path(r'^admin/', admin.site.urls),   # NOQA
    # CMS - should be last
    re_path(r'^', include('cms.urls')),
    {%- endif %}
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    {% if cookiecutter.use_django_cms == 'y' -%}
    # This is only needed when using runserver.
    urlpatterns = [
        re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}, name="media"),
        ] + staticfiles_urlpatterns() + urlpatterns

    {%- endif %}

    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
