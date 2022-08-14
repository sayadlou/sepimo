from azbankgateways.urls import az_bank_gateways_urls
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from apps.core.sitemaps import PostSitemap

sitemaps = {
    'blog': PostSitemap
}

urlpatterns = [
    path('', include(('apps.core.urls', 'apps.core'), namespace='core')),
    path('account/', include(('apps.account.urls', 'apps.account'), namespace='account')),
    path('blog/', include(('apps.blog.urls', 'apps.blog'), namespace='blog')),
    path('store/', include(('apps.store.urls', 'apps.store'), namespace='store')),
    path('captcha/', include('captcha.urls')),
    path('contact_us/', include(('apps.contact_us.urls', 'apps.contact_us'), namespace='contact_us')),
    path('bankgateways/', az_bank_gateways_urls()),
    path('tinymce/', include('tinymce.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]
