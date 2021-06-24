from django.urls import include, path
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    path('bbs/', include('bbs.urls')),
    path('admin/', admin.site.urls),
    #path('', RedirectView.as_view(url='/bbs/')),
]
