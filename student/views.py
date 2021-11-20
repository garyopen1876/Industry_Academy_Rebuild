from django.shortcuts import render, redirect
from .models import *
from web.models import Profile
from manager.models import Function


# 媒合系統-學生頁面
def show_student(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.STUDENT:
            check_user = Student.objects.filter(user=request.user)
            check_upload = Function.objects.filter(function='履歷與投遞公司')
            check_sort = Function.objects.filter(function='履歷審核狀態與選填志願')
            check_result = Function.objects.filter(function='學生放榜結果')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'student.html', locals())
    else:
        return redirect('')


# 學生-個人資料
def student_information(request, student_id=None):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.STUDENT:
            check_user = Student.objects.filter(user=request.user)
            if check_user.exists():
                unit = Student.objects.get(user=request.user)
            else:
                message = '使用者個人資料未定義!'
                return redirect('/system/student/studentEdit')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'student_information.html', locals())
    else:
        return redirect('')


# 學生-編輯個人資訊
def student_edit(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.STUDENT:
            message = '請填入個人資料！'
            check_user = Student.objects.filter(user=request.user)
            if check_user.exists():
                unit = Student.objects.get(user=request.user)
            if request.method == 'POST':
                if check_user.exists():
                    unit.name = request.POST['name']
                    unit.class_name = request.POST['class']
                    unit.phone = request.POST['phone']
                    unit.email = request.POST['email']
                    unit.save()
                    message = '修改資料成功！'
                else:
                    s_user = request.user
                    s_name = request.POST['name']
                    s_class = request.POST['class']
                    s_phone = request.POST['phone']
                    s_email = request.POST['email']
                    unit = Student.objects.create(user=s_user, name=s_name, class_name=s_class, phone=s_phone,
                                                  email=s_email)
                    unit.save()
                    message = '資料上傳成功！'
            else:
                message = '請個人輸入資料！'
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'student_edit.html', locals())
    else:
        return redirect('')
