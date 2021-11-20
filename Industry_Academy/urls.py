"""Industry_Academy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from web import views as web

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', web.index, name='index'),
    path('logout/', web.logout, name='logout'),
    path('change_password/', web.change_password, name='change_password'),

    #path('personal_index/', web.personal_index, name='personal_index'),

    #path('news/list/', web.news_list, name='news_list'),
    #path('news/detail/<int:message_id>/', web.news_detail, name='news_detail'),

    #path('student/', include('student.urls')),
    path('company/', include('company.urls')),
    #path('manager/', include('manager.urls')),
    #path('tutor/', include('tutor.urls')),
    #path('match/', include('match.urls')),
    #path('inter_ship/', include('inter_ship.urls')),
    #path('message_board/', include('message_board.urls')),


    #path('accounts/NID/login/callback/', web.nid_callback),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
