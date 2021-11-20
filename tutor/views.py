from django.shortcuts import render, redirect
from .models import *


# 媒合系統-導師頁面
def show_tutor(request):
    if request.user.is_authenticated:
        if request.user.profile.role in (Tutor.UNIVERSITY_TUTOR, Tutor.COMPANY_TUTOR1, Tutor.COMPANY_TUTOR2):
            check_user = Tutor.objects.filter(user=request.user)
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'tutor.html', locals())
    else:
        return redirect('')


# 導師-個人資料
def tutor_information(request):
    if request.user.is_authenticated:
        if request.user.profile.role in (Tutor.UNIVERSITY_TUTOR, Tutor.COMPANY_TUTOR1, Tutor.COMPANY_TUTOR2):
            check_user = Tutor.objects.filter(user=request.user)
            if check_user.exists():
                unit = Tutor.objects.get(user=request.user)
            else:
                message = '使用者個人資料未定義!'
                return redirect('/system/tutor/tutorEdit')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'tutor_information.html', locals())
    else:
        return redirect('')


# 導師-編輯個人資訊
def tutor_edit(request):
    if request.user.is_authenticated:
        if request.user.profile.role in (Tutor.UNIVERSITY_TUTOR, Tutor.COMPANY_TUTOR1, Tutor.COMPANY_TUTOR2):
            message = '請填入個人資料！'
            check_user = Tutor.objects.filter(user=request.user)
            if check_user.exists():
                unit = Tutor.objects.get(user=request.user)
            if request.method == 'POST':
                if check_user.exists():
                    unit.name = request.POST['name']
                    unit.phone = request.POST['phone']
                    unit.email = request.POST['email']
                    unit.save()
                    message = '修改資料成功！'
                else:
                    t_user = request.user
                    t_name = request.POST['name']
                    t_phone = request.POST['phone']
                    t_email = request.POST['email']
                    t_role = request.user.profile.role
                    unit = Tutor.objects.create(user=t_user, name=t_name, phone=t_phone, email=t_email, category=t_role)
                    unit.save()
                    message = '資料上傳成功！'
            else:
                message = '請個人輸入資料！'
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'tutor_edit.html', locals())
    else:
        return redirect('')
