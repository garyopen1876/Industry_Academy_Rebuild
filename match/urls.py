from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [

    path('', views.match),
    path('managerStudentCompany/', views.manager_student_company),

    path('companyResume/', views.show_company_resume_list),
    path('companyReview/<int:resume_id>/', views.company_review),
    path('companyRemark/<int:resume_id>/', views.company_remark),
    path('companyAdmission/', views.company_admission),
    path('companyResult/', views.company_result),

    path('studentUpload/', views.student_upload),
    path('studentSortInformation/', views.student_sort_information),
    path('studentFeedback/<int:feedback_id>/', views.student_feedback),
    path('studentSort/', views.student_sort),
    path('studentResult/', views.student_result),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
