from django.urls import path, include

from django.contrib import admin
from django.views.generic import TemplateView
admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path('pushbots-worker.js', (TemplateView.as_view(template_name="pushbots-worker.js",content_type='application/javascript', )), name='pushbots-worker.js'),
]
