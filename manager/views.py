import datetime  # 時間
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from web.models import Profile, Message
from company.models import Company, VacancyRequirement


# True False切換
def function_switch(unit):
    unit.switch = not unit.switch
    unit.save()


# 媒合系統-助教頁面
def show_manager(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.MANAGER:
            message = '登入成功！'
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'manager.html', locals())
    else:
        return redirect('')


# 助教-新增用戶
def create_user(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.MANAGER:
            if request.method == 'POST':
                user_id = request.POST['userID']
                password = request.POST['password']
                check = request.POST['check']
                role = request.POST.get('role')
                if User.objects.filter(username=user_id).exists():
                    message = '此用戶已經存在！'
                else:
                    if password == check:
                        if role == '2' or role == '4':
                            user = User.objects.create(username=user_id)
                            user.set_password(password)
                            unit = Profile(user=user)
                            unit.role = role
                            user.save()
                            unit.save()
                            message = '新用戶建置完成！'
                        else:
                            message = '請選擇身分！'
                    else:
                        message = '新密碼格式錯誤 or 兩次密碼不正確！'
            else:
                message = '請輸入新用戶資料！'
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'creat_user.html', locals())
    else:
        return redirect('')


# 助教-公佈欄管理
def post_manage(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.MANAGER:
            message_all = Message.objects.all().order_by('-created')
            message_size = len(message_all)
            message_units = Message.objects.filter().order_by('-created')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'post_manage.html', locals())
    else:
        return redirect('')


# 助教-公佈欄新增
def add_post(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.MANAGER:
            if request.method == 'POST':
                message_file = request.FILES.get('messageFile')
                if message_file is not None and message_file.content_type.split('/')[1] != 'pdf':
                    message = '上傳格式錯誤！格式必須為 pdf 檔！'
                else:
                    message_title = request.POST['messageTitle']
                    message_context = request.POST['messageContext']
                    post_message = Message.objects.create(title=message_title, content=message_context,
                                                          created=datetime.datetime.now())
                    post_message.url = message_file
                    post_message.save()
                    return redirect('/system/manager/postManage')
            else:
                message = '新增公佈欄訊息！'
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'add_post.html', locals())
    else:
        return redirect('')


# 助教-公佈欄編輯或刪除
def delete_post(request, post_id=None):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.MANAGER:
            unit = Message.objects.get(id=post_id)
            if request.method == 'POST':
                unit.delete()
                return redirect('/system/manager/postManage')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'delete_post.html', locals())
    else:
        return redirect('')


# 助教-編輯公佈欄
def edit_post(request, post_id=None):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.MANAGER:
            unit = Message.objects.get(id=post_id)
            if request.method == 'POST':
                message_file = request.FILES.get('messageFile')
                if message_file is not None and message_file.content_type.split('/')[1] != 'pdf':
                    message = '上傳格式錯誤！格式必須為 pdf 檔！'
                else:
                    unit.title = request.POST['messageTitle']
                    unit.content = request.POST['messageContext']
                    if message_file is not None:
                        unit.url.delete()
                        unit.url = message_file
                    unit.message_Created = datetime.datetime.now()
                    unit.save()
                    return redirect('/system/manager/postManage')
            else:
                message = '修改公佈欄訊息！'
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'edit_post.html', locals())
    else:
        return redirect('')


# 助教-功能排程
def schedule(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.MANAGER:
            student_units = Function.objects.filter(role='學生').order_by('id')
            company_units = Function.objects.filter(role='公司').order_by('id')
            if request.method == 'POST':
                function_ob = Function.objects.all()
                for unit in function_ob:
                    if unit.function in request.POST:
                        function_switch(unit)
            else:
                message = '請選擇要開關的功能！'
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'schedule.html', locals())
    else:
        return redirect('')


# 助教-企業資訊
def company_list(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.MANAGER:
            company_ob = Company.objects.all()
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'company_list.html', locals())
    else:
        return redirect('')


# 助教-企業詳細資訊
def company_list_detail(request, manager_company_detail_id=None):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.MANAGER:
            unit = Company.objects.get(id=manager_company_detail_id)
            check_vacancy = VacancyRequirement.objects.filter(name=unit)
            if check_vacancy.exists():
                show_vacancy = check_vacancy
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'company_list_detail.html', locals())
    else:
        return redirect('')
