from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [

    path('', views.report),
    path('student/', views.report_student),
    path('manager/', views.report_manager),
    path('tutor/', views.report_tutor),
    path('detail/<int:inter_ship_id>/', views.report_detail),
    path('companyTutor/feedback/<int:report_id>/', views.company_tutor_feedback),
    path('universityTutor/feedback/<int:report_id>/', views.university_tutor_feedback),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)