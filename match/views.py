from django.shortcuts import render, redirect
from .models import *
from web.models import Profile
from company.models import Company, VacancyRequirement, ContactPerson
from student.models import Resume
from manager.models import Function


# 數字檢測(學生-志願序填表,企業-履歷審察、結果)
def sort_check(sort_check_list):
    check_num = 0
    sort_num = 1
    while check_num < len(sort_check_list):
        # 泡泡排序
        for i in range(0, len(sort_check_list) - 1):  # 有n-1回合(n為數字個數)
            for j in range(0, len(sort_check_list) - 1 - i):  # 每回合進行比較的範圍
                if int(sort_check_list[j]) > int(sort_check_list[j + 1]):  # 是否需交換
                    tmp = sort_check_list[j]
                    sort_check_list[j] = sort_check_list[j + 1]
                    sort_check_list[j + 1] = tmp
        # 確認數字順序並無問題
        for x in sort_check_list:
            if int(x) <= 0:
                return 1
            elif int(x) == sort_num:
                check_num = check_num + 1
                sort_num = sort_num + 1
            else:
                return 1
    return 0


# 學生-履歷與投遞公司
def student_upload(request, company_id=None):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.STUDENT and Function.objects.get(function='履歷與投遞公司').switch is True:
            check_user = Student.objects.filter(user=request.user)
            if check_user.exists():
                company_all = Company.objects.all().order_by('id')
                company_size = len(company_all)
                company_units = Company.objects.filter().order_by('id')
                # 網頁顯示部份
                student = Student.objects.get(user=request.user)
                check_resume = Resume.objects.filter(student=student)
                show_check = 0
                if check_resume.exists():  # 判斷是否已經生成Resume資料
                    show_check = 1
                    resume_ob = Resume.objects.get(student=student)
                else:
                    message = '你尚未投遞履歷'

                # post部份
                check_admission = Admission.objects.filter(student=student)
                if request.method == 'POST':
                    resume = request.FILES.get('resume')
                    # 選擇上傳履歷
                    if 'postResume' in request.POST:
                        # 履歷是否符合標準
                        if request.FILES.get('resume') is not None:
                            if resume.content_type.split('/')[1] != 'pdf':
                                message = '上傳格式錯誤！格式必須為pdf檔！'
                            else:
                                # 生成或修改Resume以及Admission
                                if check_admission.exists():
                                    unit = Resume.objects.get(student=student)
                                    unit.resume.delete()
                                    unit.resume = resume
                                    unit.save()
                                    message = '修改上傳成功！'
                                else:
                                    Resume.objects.create(student=student)
                                    unit = Resume.objects.get(student=student)
                                    unit.resume = resume
                                    unit.save()
                                    message = '履歷上傳成功！'
                                return redirect('/match/studentUpload')
                        else:
                            message = '請選擇檔案！ 格式為 pdf 檔!'
                    # 選擇填寫投遞公司
                    elif 'postAdmission' in request.POST:
                        if check_resume.exists():
                            unit = Resume.objects.get(student=student)
                            if check_admission.exists():
                                Admission.objects.filter(student=student).delete()
                                companys = request.POST.getlist('fcompany')
                                vacancy = request.POST.getlist('fvacancy')
                                unit.company.clear()
                                for n in companys:
                                    company = Company.objects.get(name=n)
                                    unit.company.add(company)
                                    Admission.objects.create(student=student, company=company)
                                    admission = Admission.objects.get(student=student, company=company)
                                    vacancy = request.POST['vacancy' + company.user.username]
                                    admission.vacancy = vacancy
                                    admission.save()
                                unit.save()
                                message = '投遞公司修改成功！'
                            else:
                                companys = request.POST.getlist('fcompany')
                                vacancy = request.POST.getlist('fvacancy')
                                for n in companys:
                                    company = Company.objects.get(name=n)
                                    unit.company.add(company)
                                    Admission.objects.create(student=student, company=company)
                                    admission = Admission.objects.get(student=student, company=company)
                                    vacancy = request.POST['vacancy' + company.user.username]
                                    admission.vacancy = vacancy
                                    admission.save()
                                message = '投遞公司上傳成功！'
                        else:
                            message = '請先上傳履歷!'
            else:
                message = '使用者個人資料未定義!'
                return redirect('/student/studentEdit')
        else:
            message = '身分錯誤！請先登出切換身分 or 功能未開放！'
            return redirect('/personal_index')
        return render(request, "student_upload.html", locals())
    else:
        return redirect('')


# 學生-履歷審核狀態及填寫企業公司志願排序
def student_sort_information(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.STUDENT and Function.objects.get(function='履歷審核狀態與選填志願').switch is True:
            check_user = Student.objects.filter(user=request.user)
            if check_user.exists():
                student = Student.objects.get(user=request.user)
                check_resume = Resume.objects.filter(student=student)
                check_admission = Admission.objects.filter(student=student)
                if check_resume.exists() and check_admission.exists():
                    admission = check_admission
                else:
                    message = '您並未在期限內上傳個人履歷，請聯絡助教詳談!'
            else:
                message = '使用者個人資料未定義!'
                return redirect('/student/studentEdit')
        else:
            message = '身分錯誤！請先登出切換身分 or 功能尚未開放！'
            return redirect('/personal_index')
        return render(request, 'student_sort_information.html', locals())
    else:
        return redirect('')


# 學生-履歷審查回饋
def student_feedback(request, feedback_id=None):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.STUDENT and Function.objects.get(function='履歷審核狀態與選填志願').switch is True:
            check_user = Student.objects.filter(user=request.user)
            if check_user.exists():
                student = Student.objects.get(user=request.user)
                check_admission = Admission.objects.filter(id=feedback_id, student=student)
                if check_admission.exists():
                    unit = Admission.objects.get(id=feedback_id)
                else:
                    message = '並未投此公司履歷！'
                    return redirect('/student')
            else:
                message = '使用者個人資料未定義!'
                return redirect('/student/studentEdit')
        else:
            message = '身分錯誤！請先登出切換身分 or 功能尚未開放！'
            return redirect('/personal_index')
        return render(request, 'student_feedback.html', locals())
    else:
        return redirect('')


# 學生-志願序填表
def student_sort(request):
    sort_check_list = []
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.STUDENT and Function.objects.get(function='履歷審核狀態與選填志願').switch is True:
            check_user = Student.objects.filter(user=request.user)
            if check_user.exists():
                student_ob = Student.objects.get(user=request.user)
                check_resume = Resume.objects.filter(student=student_ob)
                check_admission = Admission.objects.filter(student=student_ob)
                if check_resume.exists() and check_admission.exists():
                    resume_ob = Resume.objects.get(student=student_ob)
                    if request.method == 'POST':
                        # 不重複測試
                        sort_check_list.clear()
                        for tag in resume_ob.company.all():
                            v_sort = request.POST['sort' + tag.name]
                            if v_sort != '':
                                sort_check_list.append(v_sort)
                        if sort_check(sort_check_list) == 1:
                            message = '排序輸入錯誤!'
                        else:
                            for tag in resume_ob.company.all():
                                v_sort = request.POST['sort' + tag.name]
                                unit = Admission.objects.get(student=student_ob, company=tag)
                                unit.volunteer_order = v_sort
                                unit.save()
                            message = '資料上傳成功!'
                            return redirect('/match/studentSortInformation')
                else:
                    message = '您並未在期限內上傳個人履歷，請聯絡助教詳談!'
            else:
                message = '使用者個人資料未定義!'
                return redirect('/student/studentEdit')
        else:
            message = '身分錯誤！請先登出切換身分 or 功能尚未開放！'
            return redirect('/personal_index')
        return render(request, 'student_sort.html', locals())
    else:
        return redirect('')


# 企業-履歷審察
def show_company_resume_list(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.COMPANY and Function.objects.get(function='履歷審察').switch is True:
            check_user = ContactPerson.objects.filter(user=request.user)
            if check_user.exists():
                check_company = Company.objects.filter(contact_persons=check_user.get())
                if check_company.exists():
                        units = check_company.get()
                else:
                    message = '使用者個人資料未定義 or 功能尚未開放！'
                    return redirect('/company/companyEdit')
            else:
                message = '無此負責人'
                return redirect('/company')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/personal_index')
        return render(request, 'show_company_resume_list.html', locals())
    else:
        return redirect('')


# 企業-審查履歷與回饋
def company_review(request, resume_id=None):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.COMPANY and Function.objects.get(function='履歷審察').switch is True:
            check_user = ContactPerson.objects.filter(user=request.user)
            if check_user.exists():
                check_company = Company.objects.filter(contact_persons=check_user.get())
                if check_company.exists():
                    company = Company.objects.get(contact_persons=check_user.get())
                    student = Student.objects.get(user=Resume.objects.get(id=resume_id).student.user)
                    check_admission = Admission.objects.filter(student=student, company=company)
                    if check_admission.exists():
                        unit = Admission.objects.get(student=student, company=company)
                        if request.method == 'POST':
                            unit.review = request.POST['review']
                            unit.feedback = request.POST['feedback']
                            unit.save()
                            message = '修改上傳成功！'
                        else:
                            message = '請輸入資料！'
                    else:
                        message = '這位學生沒有投這間公司履歷！'
                        return redirect('/company/')
                else:
                    message = '使用者個人資料未定義!'
                    return redirect('/company/companyEdit')
            else:
                message = '無此負責人'
                return redirect('/company')
        else:
            message = '身分錯誤！請先登出切換身分 or 功能尚未開放！'
            return redirect('/personal_index')
        return render(request, 'company_review.html', locals())
    else:
        return redirect('')


# 企業-備註
def company_remark(request, resume_id=None):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.COMPANY and Function.objects.get(function='履歷審察').switch is True:
            check_user = ContactPerson.objects.filter(user=request.user)
            if check_user.exists():
                check_company = Company.objects.filter(contact_persons=check_user.get())
                if check_company.exists():
                    company = Company.objects.get(contact_persons=check_user.get())
                    student = Student.objects.get(user=Resume.objects.get(id=resume_id).student.user)
                    check_admission = Admission.objects.filter(student=student, company=company)
                    if check_admission.exists():
                        unit = Admission.objects.get(student=student, company=company)
                        if request.method == 'POST':
                            unit.remark = request.POST['remark']
                            unit.save()
                            message = '修改上傳成功！'
                        else:
                            message = '請輸入資料！'
                    else:
                        message = '這位學生沒有投這間公司履歷！'
                        return redirect('/company/')
                else:
                    message = '使用者個人資料未定義!'
                    return redirect('/company/companyEdit')
            else:
                message = '無此負責人'
                return redirect('/company')
        else:
            message = '身分錯誤！請先登出切換身分 or 功能尚未開放！'
            return redirect('/personal_index')
        return render(request, 'company_remark.html', locals())
    else:
        return redirect('')


# 企業-正備取結果
def company_admission(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.COMPANY and Function.objects.get(function='正備取結果').switch is True:
            check_user = ContactPerson.objects.filter(user=request.user)
            if check_user.exists():
                check_company = Company.objects.filter(contact_persons=check_user.get())
                if check_company.exists():
                    units = check_company.get()
                    check_vacancy = VacancyRequirement.objects.filter(company=units).all()
                    check_vacancy_list = []  # 檢測超過需求量的陣列

                    if request.method == 'POST':
                        # 檢測是否有按照規範填寫
                        for unit in units.resume_set.all():
                            unit_vacancy = []  # 紀錄該學生的錄取職業以及備取順序的陣列(為正取會輸入0)
                            unit_vacancy_result = request.POST.get(unit.student.user.username + 'VacancyResult')
                            unit_sort_result = request.POST.get(unit.student.user.username + 'Sort')

                            # 先判斷此admission是否有填入職位
                            if unit_vacancy_result is not None:
                                unit_vacancy.append(unit_vacancy_result)
                                if unit_sort_result is None:
                                    message = unit.student.name + ' 只有填錄取職位，並未填正備取'
                                    return render(request, 'company_admission.html', locals())
                                elif unit_sort_result == '正取':
                                    unit_vacancy.append('0')  # 屬於正取 輸入零
                                elif unit_sort_result == '備取':
                                    if request.POST.get(unit.student.user.username + 'Rank') != '':
                                        # 如果為備取 紀錄備取數字(之後判斷順序是否錯誤)
                                        unit_vacancy.append(request.POST.get(unit.student.user.username + 'Rank'))
                                    else:
                                        message = unit.student.name + ' 的備取 並未填入數字!!(備取一定要有順序)'
                                        return render(request, 'company_admission.html', locals())
                                # 存入檢查陣列之中
                                check_vacancy_list.append(unit_vacancy)

                        # 檢測職位正取數列是否超過需求量
                        for vacancy in check_vacancy:
                            vacancy_waiting_list = []  # 檢查備取判斷順序的陣列
                            vacancy_number_count = 0
                            for vacancyList in check_vacancy_list:
                                # 確認職位名稱(分類)
                                if vacancyList[0] == vacancy.name:
                                    # 為正取時，計算是否超過職位需求量
                                    if vacancyList[1] == '0':
                                        vacancy_number_count = vacancy_number_count + 1
                                    else:
                                        vacancy_waiting_list.append(vacancyList[1])
                            # 當超過需求量時
                            if vacancy_number_count > vacancy.number:
                                message = vacancy.name + ' 的正取量超過職位數量，請至新增職位資訊更改數量'
                                return render(request, 'company_admission.html', locals())
                            # 備取順序出錯
                            elif sort_check(vacancy_waiting_list) != 0:
                                message = vacancy.name + ' 的備取排序出錯，請按照正確順序填寫(1、2、3....依此類推) '
                                return render(request, 'company_admission.html', locals())

                        # 通過所有檢測後儲存資料
                        for unit in units.resume_set.all():
                            check_admission = Admission.objects.filter(student=unit.student)
                            if check_admission.exists():
                                unit_admission = Admission.objects.get(student=unit.student, company=units)
                                unit_admission.vacancy_result = \
                                    request.POST.get(unit.student.user.username + 'VacancyResult')
                                unit_admission.sort = \
                                    str(request.POST.get(unit.student.user.username + 'Sort')) + \
                                    str(request.POST.get(unit.student.user.username + 'Rank'))
                                unit_admission.save()
                        message = '儲存成功'
                    else:
                        message = '請填寫正備取！'
                else:
                    message = '使用者個人資料未定義 or 功能尚未開放！'
                    return redirect('/company/companyEdit')
            else:
                message = '無此負責人'
                return redirect('/company')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/personal_index')
        return render(request, 'company_admission.html', locals())
    else:
        return redirect('')


# 企業-放榜結果
def company_result(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.COMPANY and Function.objects.get(function='企業放榜結果').switch is True:
            check_user = ContactPerson.objects.filter(user=request.user)
            if check_user.exists():
                check_company = Company.objects.filter(contact_persons=check_user.get())
                if check_company.exists():
                    company_ob = check_company.get()
                    check_result = Result.objects.filter(company=company_ob)
                    if check_result.exists():
                        show_result = check_result
                        if request.method == 'POST':
                            for unit in show_result:
                                vacancy = request.POST[unit.student.user.username]
                                unit.result_vacancy = vacancy
                                unit.save()
                            message = '儲存完畢!'
                    else:
                        message = '未有員工'
                else:
                    message = '企業資料未定義!'
                    return redirect('/company/companyEdit')
            else:
                message = '無此負責人'
                return redirect('/company')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/personal_index')
        return render(request, 'company_result.html', locals())
    else:
        return redirect('')


# 助教-學生投遞公司總覽
def manager_student_company(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.MANAGER:
            company_ob = Company.objects.all()
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/personal_index')
        return render(request, 'manager_student_company.html', locals())
    else:
        return redirect('')


# 媒合演算法
def match_code():
    print("ok")


# 媒合
def match(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.MANAGER:
            result_ob = Result.objects.all()
            if request.method == 'POST':
                message = '媒合!'
                match_code()
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('')
        return render(request, 'match.html', locals())
    else:
        return redirect('')


# 學生-放榜結果
def student_result(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.STUDENT and Function.objects.get(function='學生放榜結果').switch is True:
            check_user = Student.objects.filter(user=request.user)
            if check_user.exists():
                show_result = []
                student_ob = Student.objects.get(user=request.user)
                check_result = Result.objects.filter(student=student_ob)
                if student_ob.give_up is True:
                    message = '您已放棄本次媒合，如有疑問請聯絡助教!'
                elif check_result.exists():
                    result_ob = Result.objects.get(student=student_ob)
                    show_result.append('恭喜 '+result_ob.student.name+' 同學 錄取:  ' +
                                       result_ob.company.name)
                    message = '恭喜您!脫穎而出!'
                    if result_ob.result_vacancy != '':
                        show_result.append('職位: '+result_ob.result_vacancy)
                    else:
                        show_result.append('職位尚未出來，請耐心等待!')
                else:
                    message = '您尚未錄取，請耐心等待!'
                # 放棄名額
                if request.method == 'POST' and student_ob.give_up is not True:
                    student_ob.give_up = True
                    student_ob.save()
                    if check_result.exists():
                        check_result.get().delete()
                        match_code()
                    message = '您已放棄本次媒合，如有疑問請聯絡助教!'
            else:
                message = '使用者個人資料未定義 or 功能尚未開放！'
                return redirect('/student/studentEdit')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/personal_index')
        return render(request, 'student_result.html', locals())
    else:
        return redirect('')
