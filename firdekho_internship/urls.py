
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import MyLoginView
from django.views.generic import RedirectView
urlpatterns = [
    path('', RedirectView.as_view(url='login', permanent=True), name='index'),
    path('admin/', admin.site.urls),
    path('login/', MyLoginView.as_view(template_name='registration/login.html'), name="login1"),
    path('core/', include('core.urls', namespace="core")),
    path('accounts/', include('django.contrib.auth.urls')),

]
