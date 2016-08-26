"""vedomosti2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Offshores.views import *
from Users.views import *
from django.conf import settings
from django.conf.urls import patterns
from django.views.static import serve
import uuid


urlpatterns = [
    url(r'^vedadmin/', admin.site.urls),
    url(r'^$', home),
    url(r'^BO/$', BO),
    url(r'^AB/$', AB),
    url(r'^AO/$', AO),
    url(r'^login/$', form),
    url(r'^user/login/$', login),
    url(r'^faq/$', faq),
    url(r'^offshore/(?P<slug>[-\w]+)/$', InstanceView.as_view(model = Offshore, template_name = 'off_detail.html'), name = 'offshore'),
    url(r'^beneficiary/(?P<slug>[-\w]+)/$', InstanceView.as_view(model = Beneficiary, template_name = 'ben_detail.html'), name = 'beneficiary'),
    url(r'^asset/(?P<slug>[-\w]+)/$', InstanceView.as_view(model = Asset, template_name = 'asset_detail.html'), name = 'asset'),
    url(r'^user/logout/$', logout),
    
]

if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )



# if settings.DEBUG:
#     urlpatterns += patterns('',
#         (r'%s(?P<path>.*)' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
#     )


if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
   ]
