import logging
from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse
from Industry_Academy.settings import NID_CLIENT_ID  # 使用setting資料
from .models import *
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from manager.models import Message


logger = logging.getLogger('debug')


# 首頁
def index(request):
    return render(request, 'homepage.html', locals())


# 公佈欄
def news_list(request):
    message_units = Message.objects.filter().order_by('-created')
    return render(request, "post.html", locals())


# 公佈欄 詳細訊息
def news_detail(request, detail_id=None):
    unit = Message.objects.get(id=detail_id)
    return render(request, 'detail.html', locals())


# 媒合系統登入
def personal_index(request):
    nid_login_url = 'https://opendata.fcu.edu.tw/fcuOauth/Auth.aspx?client_id=' + NID_CLIENT_ID + \
                    '&client_url=' + request.scheme + '://' + request.get_host() + '/accounts/NID/login/callback/'
    if request.user.is_authenticated:  # 如果有登入，不需重複登入
        if request.user.profile.role == Profile.STUDENT:
            return redirect('/student')
        elif request.user.profile.role == Profile.COMPANY:
            return redirect('/company')
        elif request.user.profile.role == Profile.MANAGER:
            return redirect('/manager')
        elif request.user.profile.role in (Profile.UNIVERSITY_TUTOR, Profile.COMPANY_TUTOR1, Profile.COMPANY_TUTOR2):
            return redirect('/tutor')
        else:
            message = '身分錯誤！請先登出切換身分！'

    if request.method == 'POST':  # 如果是 <system.html> 傳送登入訊息
        user_id = request.POST['userID']  # 取得帳號
        password = request.POST['password']  # 取得密碼
        user = auth.authenticate(username=user_id, password=password, request=request)  # 使用者驗證
        if user is not None:
            if user.is_active:
                if user.profile.role == Profile.STUDENT:
                    auth.login(request, user)
                    message = '登入成功！'
                    return redirect('/student')
                elif user.profile.role == Profile.COMPANY:
                    auth.login(request, user)
                    message = '登入成功！'
                    return redirect('/company')
                elif user.profile.role == Profile.MANAGER:
                    auth.login(request, user)
                    message = '登入成功！'
                    return redirect('/manager')
                elif user.profile.role in (Profile.UNIVERSITY_TUTOR, Profile.COMPANY_TUTOR1, Profile.COMPANY_TUTOR2):
                    auth.login(request, user)
                    message = '登入成功！'
                    return redirect('/tutor')
                else:
                    message = '登入身分錯誤！'
            else:
                message = '帳號及密碼不能為空！'
        else:
            message = '登入失敗！'
    return render(request, 'system.html', locals())


# 登出
def logout(request):
    auth.logout(request)
    return redirect('/')


# 修改密碼
def change_password(request):
    if request.user.is_authenticated:
        if request.user.profile.role in (Profile.COMPANY, Profile.COMPANY_TUTOR1, Profile.COMPANY_TUTOR2):
            if request.method == 'POST':
                old = request.POST['old']
                new = request.POST['new']
                check = request.POST['check']
                user = auth.authenticate(username=request.user.username, password=old)
                if user is not None:
                    if new == check:
                        user.set_password(new)
                        user.save()
                        message = '修改密碼成功！'
                        return redirect('/personal_index')
                    else:
                        message = '新密碼格式錯誤 or 兩次密碼不正確！'
                else:
                    message = '舊密碼錯誤！'
            else:
                message = '請輸入舊密碼與新密碼！'
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/personal_index')
        return render(request, 'change_password.html', locals())
    else:
        return redirect('')


# 聯絡我們
def show_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            complete_msg = '******此為系統自動發信，請勿直接回覆******\n' + message + '\n聯繫方式：' + sender_email \
                           + '\n******此為系統自動發信，請勿直接回覆******\n'
            try:
                logger.debug(sender_email)
                send_mail(subject, complete_msg, sender_email, ['cassandrachan108@gmail.com'], fail_silently=False,)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse('Thank you for contacting us.')
    else:
        form = ContactForm()
    return render(request, 'contact.html', locals())

