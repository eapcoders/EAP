"""rockstars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, re_path
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from app import views as view


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', view.home, name='home'),
    url(r'^about-us/', view.about_us),
    url(r'^flight-booking/', view.flight_booking),
    url(r'^train-booking/', view.train_booking),
    url(r'^bus-booking/', view.bus_booking),
    url('^buy-item/(?P<item_id>\d+)/$', view.buy),
    url(r'^fuel/', view.fuel),
    url(r'^fertilizers/', view.fertilizers),
    url(r'^recycle/', view.recycle),
    url(r'^dbmall/', view.dbmall),
    url(r'^reports/', view.reports),
    url(r'^bid/', view.bid),
    url(r'^transactions/', view.transactions),
    url(r'^investments/', view.investments),
    url(r'^transfer-credit/', view.transfer_credit),
    url(r'^go-green-kitty/', view.go_green_kitty),
    re_path('login/', auth_views.LoginView.as_view(), {
        'template_name': "registration/login.html"},
        name='login'),
    re_path('logout/', auth_views.LogoutView.as_view(),
        {'next_page': '/'}, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
