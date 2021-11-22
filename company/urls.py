from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [

    path('', views.show_company),
    path('companyInformation/', views.company_information),
    path('companyEdit/', views.company_edit),
    path('companyContactPersonInformation/', views.company_contact_person_information),
    path('companyContactPersonEdit/', views.company_contact_person_edit),
    path('companyUpload/', views.company_upload),
    path('companyVacancyNew/', views.company_vacancy_new),
    path('companyVacancyEdit/<int:company_vacancy_edit_id>/', views.company_vacancy_edit),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
