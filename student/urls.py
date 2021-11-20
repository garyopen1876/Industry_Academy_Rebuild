from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [

    path('', views.show_student),
    path('studentInformation/', views.student_information),
    path('studentEdit/', views.student_edit),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
