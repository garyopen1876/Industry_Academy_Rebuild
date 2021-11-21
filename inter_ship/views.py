import datetime
from django.shortcuts import render, redirect
from Industry_Academy.settings import NID_CLIENT_ID  # 使用setting資料
from .models import *
from django.http import HttpResponse
from student.models import Student, InterShip
from web.models import Profile
from tutor.models import Tutor


# 實習報告-導向
def report(request):
    nid_login_url = 'https://opendata.fcu.edu.tw/fcuOauth/Auth.aspx?client_id=' + NID_CLIENT_ID + \
                    '&client_url=' + request.scheme + '://' + request.get_host() + '/accounts/NID/login/callback/'
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.STUDENT:
            return redirect('/inter_ship/student')
        elif request.user.profile.role == Profile.MANAGER:
            return redirect('/inter_ship/manager')
        elif request.user.profile.role in (Profile.UNIVERSITY_TUTOR, Profile.COMPANY_TUTOR1, Profile.COMPANY_TUTOR2):
            return redirect('/inter_ship/tutor')
        else:
            return HttpResponse("此為學生功能!!")
    else:
        return redirect(nid_login_url)


# 實習報告-學生
def report_student(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.STUDENT:
            check_user = Student.objects.filter(user=request.user)
            if check_user.exists():
                check_inter_ship = InterShip.objects.filter(student=check_user.get())
                if check_inter_ship.exists():
                    check_month_report = MonthReport.objects.filter(student=check_user.get())
                    if check_month_report.exists():
                        month_report = check_month_report.all().order_by('deadline')
                        deadline_compare = datetime.datetime.now().date()
                        # 上傳實習報告
                        if request.method == 'POST':
                            for a_report in month_report:
                                if 'report' + str(a_report.id) + 'button' in request.POST:
                                    # 報告是否符合標準
                                    check_report = request.FILES.get('report' + str(a_report.id))
                                    if check_report is not None:
                                        if check_report.content_type.split('/')[1] != 'pdf':
                                            message = '上傳格式錯誤！格式必須為pdf檔！'
                                        else:
                                            unit = MonthReport.objects.get(student=check_user.get(),
                                                                           deadline=a_report.deadline)
                                            unit.report = check_report
                                            # 判斷是否為補交
                                            if a_report.deadline < datetime.datetime.now().date():
                                                unit.delay_upload = True
                                            unit.save()
                                            message = '上傳成功！'
                                            return redirect('/inter_ship/student')
                                    else:
                                        message = '請選擇檔案!'
                    else:
                        # 初次使用 創建月報告上傳資訊
                        inter_ship = check_inter_ship.get()

                        if inter_ship.end.year > inter_ship.start.year:
                            # 如果結束月份數字較大或等於
                            if inter_ship.end.month > inter_ship.start.month:
                                report_number = (inter_ship.end.month - inter_ship.start.month) + 12
                            # 如果結束月份數字較小或等於
                            else:
                                report_number = (12 - inter_ship.start.month + inter_ship.end.month)
                            # 計算年份
                            report_number = report_number + (inter_ship.end.year - inter_ship.start.year - 1)*12

                        elif inter_ship.end.year == inter_ship.start.year:
                            report_number = (inter_ship.end.month - inter_ship.start.month)
                        else:
                            return HttpResponse(check_user.get().name+"的實習日期有誤!")

                        # 開始建立報告檔
                        this_month = inter_ship.start.month
                        for loop in range(1, report_number):
                            this_month = this_month + 1
                            this_year = datetime.datetime.now().year
                            # 大於12月要變回1月
                            if this_month > 12:
                                this_month = this_month - 12
                                this_year = this_year + 1
                                title_name = '實習報告 '+str(12)+'月'
                            else:
                                title_name = '實習報告 ' + str(this_month - 1) + '月'
                            MonthReport.objects.create(title=title_name, student=check_user.get(),
                                                       deadline=datetime.date(this_year, this_month, 5))
                        # 最後報告
                        MonthReport.objects.create(title='成果心得報告', student=check_user.get(),
                                                   deadline=datetime.date(inter_ship.end.year, inter_ship.end.month, 5))
                        MonthReport.objects.create(title='實習成效評估表', student=check_user.get(),
                                                   deadline=datetime.date(inter_ship.end.year, inter_ship.end.month, 5))

                        return redirect('/inter_ship/student')
                else:
                    return HttpResponse("未有實習資料!")
            else:
                message = '使用者個人資料未定義!'
                return redirect('/system/student/studentEdit')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'report_student.html', locals())
    else:
        return redirect('')


# 實習報告-助教
def report_manager(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.MANAGER:
            return HttpResponse("助教系統")
    else:
        return redirect('')


# 實習報告-導師
def report_tutor(request):
    if request.user.is_authenticated:
        if request.user.profile.role in (Profile.UNIVERSITY_TUTOR, Profile.COMPANY_TUTOR1, Profile.COMPANY_TUTOR2):
            check_user = Tutor.objects.filter(user=request.user)
            if check_user.exists():
                if request.user.profile.role == Profile.UNIVERSITY_TUTOR:
                    check_student_inter_ship = InterShip.objects.filter(university_tutor=check_user.get())
                elif request.user.profile.role == Profile.COMPANY_TUTOR1:
                    check_student_inter_ship = InterShip.objects.filter(company_tutor1=check_user.get())
                else:
                    check_student_inter_ship = InterShip.objects.filter(company_tutor2=check_user.get())

                if check_student_inter_ship.exists():
                    inter_ships = check_student_inter_ship.all()
                else:
                    message = '您未有學生!'
            else:
                message = '使用者個人資料未定義!'
                return redirect('/system/tutor/tutorEdit')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'report_tutor.html', locals())
    else:
        return redirect('')


# 實習報告-導師-導生實習報告詳細內容
def report_detail(request, inter_ship_id=None):
    if request.user.is_authenticated:
        if request.user.profile.role in (Profile.UNIVERSITY_TUTOR, Profile.COMPANY_TUTOR1, Profile.COMPANY_TUTOR2):
            check_user = Tutor.objects.filter(user=request.user)
            if check_user.exists():
                inter_ship = InterShip.objects.get(id=inter_ship_id)
                check_report = MonthReport.objects.filter(student=inter_ship.student)
                if check_report.exists():
                    show_report = check_report.all()
                else:
                    message = '此學生未有實習報告！請盡速輔導!'
            else:
                message = '使用者個人資料未定義!'
                return redirect('/system/tutor/tutorEdit')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'report_detail.html', locals())
    else:
        return redirect('')


# 實習報告-企業導師回饋
def company_tutor_feedback(request, report_id=None):
    if request.user.is_authenticated:
        if request.user.profile.role in (Profile.UNIVERSITY_TUTOR, Profile.COMPANY_TUTOR1, Profile.COMPANY_TUTOR2):
            check_user = Tutor.objects.filter(user=request.user)
            if check_user.exists():
                unit = MonthReport.objects.get(id=report_id)
                # 傳送回饋(只有tutor1能夠編寫)
                if request.method == 'POST':
                    unit.company_tutor_feedback = request.POST['company_tutor_feedback']
                    unit.company_tutor_feedback_date = datetime.datetime.now()
                    unit.save()
            else:
                message = '使用者個人資料未定義!'
                return redirect('/system/tutor/tutorEdit')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'report_company_tutor_feedback.html', locals())
    else:
        return redirect('')


# 實習報告-企業導師回饋
def university_tutor_feedback(request, report_id=None):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.UNIVERSITY_TUTOR:
            check_user = Tutor.objects.filter(user=request.user)
            if check_user.exists():
                unit = MonthReport.objects.get(id=report_id)
                # 傳送回饋
                if request.method == 'POST':
                    unit.university_tutor_feedback = request.POST['university_tutor_feedback']
                    unit.university_tutor_feedback_date = datetime.datetime.now()
                    unit.save()
            else:
                message = '使用者個人資料未定義!'
                return redirect('/system/tutor/tutorEdit')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'report_university_tutor_feedback.html', locals())
    else:
        return redirect('')
