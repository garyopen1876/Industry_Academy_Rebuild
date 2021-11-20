from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [

    path('', views.show_manager),
    path('createUser/', views.create_user),
    path('postManage/', views.post_manage),
    path('postNew/', views.add_post),
    path('postDel/<int:post_del_id>/', views.delete_post),
    path('postEdit/<int:post_edit_detail_id>/', views.edit_post),
    path('schedule/', views.schedule),
    path('managerCompany/', views.company_list),
    path('managerCompanyDetail/<int:manager_company_detail_id>/', views.company_list_detail),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
