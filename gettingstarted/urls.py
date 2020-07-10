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
    path('save_push',hello.views.save_push,name="save_push"),
    path('login',hello.views.login,name="login"),
    path('signup',hello.views.signup,name="signup"),
    path('logout',hello.views.logout,name="logout"),
    path('pushbots-worker.js', (TemplateView.as_view(template_name="sw.js",content_type='application/javascript', )), name='pushbots-worker.js'),
]
