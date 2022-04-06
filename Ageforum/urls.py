from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView
from django.conf.urls import include
from forum import views as Ageforum_views
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('forum.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', TemplateView.as_view(
        template_name="sitemap.xml", content_type="application/xml")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = Ageforum_views.error_404

