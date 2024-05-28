"""
URL configuration for SpritzCollege project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include, reverse_lazy
from .views import go_home, go_control_panel, custom_login
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^$|^\/$|^home\/$", go_home, name="home"),
    
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    path ("control/", go_control_panel, name="control_panel"),

    path ("activities/", include('Activities.urls')),
    path ("profiles/", include('Profiles.urls')),
    
    path('custom_login/', custom_login, name='custom_login'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# delete_db ()
# init_db ()