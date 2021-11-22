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
                                if unit_sort_result is not None:
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
    # 公司與人數
    list_company = []
    company_ob = Company.objects.all()
    for companyUnit in company_ob:
        result_ob = Result.objects.filter(company=companyUnit).count()
        list_sort = []
        list_sort.append(companyUnit.name)
        list_sort.append(companyUnit.vacancy-result_ob)
        list_company.append(list_sort)

    # 製作志願序陣列
    list_student_sort = []
    student_ob = Student.objects.all()
    for studentUnit in student_ob:
        check_user = Admission.objects.filter(student=studentUnit)
        check_result = Result.objects.filter(student=studentUnit)
        if check_user.exists() and studentUnit.give_up is False and not(check_result.exists()):
            list_student = []
            list_student.append(studentUnit.name)
            for companyUnit in company_ob:
                sort = Admission.objects.filter(student=studentUnit, company=companyUnit)
                if sort.exists():
                    if sort.get().volunteer_order is not None and sort.get().volunteer_order is not'':
                        list_student.append(sort.get().volunteer_order)
                    else:
                        list_student.append('')
                # 不存在此生的Admission也會加入陣列
                else:
                    list_student.append('')
            # 將每個學生的陣列一一存入
            list_student_sort.append(list_student)

    # 公司錄取榜單
    list_admission = []
    admission_sort_all = Admission.objects.all()
    for AdmissionSortAll in admission_sort_all:
        if AdmissionSortAll.sort != '':
            list_sort = []
            list_sort.append(AdmissionSortAll.company.name)
            list_sort.append(AdmissionSortAll.student.name)
            list_sort.append(AdmissionSortAll.sort)
        list_admission.append(list_sort)

    # 錄取List
    list_lu = []
    # 第二批
    list_student_sort_two = []

    # 正取副程式
    def count(student, company):
        student_name = list_student_sort[student][0]
        company_name = list_company[company - 1][0]  # 公司與學生志願序裡的公司差一格
        for x in range(0, len(list_admission)):
            if list_admission[x][1] == student_name:
                if list_admission[x][0] == company_name:
                    # 辦別是否為正取
                    if list_admission[x][2][0] == '正':
                        # !!待更改成資料庫直接修改!!
                        if int(list_company[company - 1][1]) > 0:
                            leave = int(list_company[company - 1][1]) - 1
                            list_company[company - 1][1] = leave
                            reList = []
                            reList.append(company_name)
                            reList.append(student_name)
                            list_lu.append(reList)  # 錄取
                        # !!待更改成資料庫直接修改!!
                        return 1
                    else:
                        return 0

    for x in range(0, len(list_student_sort)):
        number = 1  # 志願序
        y = 1  # 公司
        while 1:
            if list_student_sort[x][y] == str(number):
                check = count(x, y)
                if check == 1:
                    break
                else:
                    number = number + 1
                    y = 1
            else:
                # 確認不超過公司長度
                if y < len(list_company):
                    y = y + 1
                else:
                    # 製作第二批名單
                    list_student_sort_two.append(list_student_sort[x])
                    break

    list_student_sort.clear()  # 清空首次陣列
    # 第二批後
    while 1:
        # 將最優秀的成績進行比較
        list_best = []
        front_sort_len = len(list_student_sort_two)
        for x in range(0, front_sort_len):
            student_name = list_student_sort_two[x][0]
            student_br = []  # 該生的備取陣列
            own_win = ''  # 該生最優秀的備取
            number = 1
            y = 1
            check_num = 300  # 檢查碼待調整(找更具指標性的)
            for z in range(0, len(list_admission)):  # 裝下該生所有備取成績
                if list_admission[z][1] == student_name:
                    # 找備取
                    if list_admission[z][2][0] == '備':
                        student_br.append(list_admission[z])
            while 1:
                if list_student_sort_two[x][y] == str(number):
                    company_name = list_company[y - 1][0]
                    # !!待更改成資料庫直接修改!!
                    company_leave = list_company[y - 1][1]
                    # 找到了 回歸
                    y = 1
                    # 探索榜單
                    for z in range(0, len(student_br)):
                        if student_br[z][0] == company_name:
                            # 確保還有餘額
                            if int(company_leave) > 0:
                                # 找出最優秀(距離剩餘最近的值)
                                win_num = int(company_leave) - int(student_br[z][2][2])
                                if win_num < check_num:
                                    check_num = int(student_br[z][2][2])
                                    own_win = student_br[z]
                    # 一一搜尋
                    number = number + 1
                # 確認不超過公司長度
                if y < len(list_company):
                    y = y + 1
                else:
                    break
            # 加入競爭並在榜單中刪除該紀錄
            if own_win != '':
                list_best.append(own_win)
                for admission in list_admission:
                    if admission[0] == own_win[0] and admission[1] == own_win[1]:
                        list_admission.remove(admission)

        # 此代表真正要錄取的學生
        win = []
        # 每個公司的錄取
        for x in range(0, len(list_company)):
            win.clear()
            # 抓出同公司的人做比較
            for y in range(0, len(list_best)):
                if list_company[x][0] == list_best[y][0]:
                    win.append(list_best[y])

            # 泡泡排序(最優秀的往前排序)
            for i in range(0, len(win) - 1):  # 有n-1回合(n為數字個數)
                for j in range(0, len(win) - 1 - i):  # 每回合進行比較的範圍
                    if int(win[j][2][2]) > int(win[j + 1][2][2]):  # 是否需交換
                        tmp = win[j]
                        win[j] = win[j + 1]
                        win[j + 1] = tmp
            # 實施錄取
            while int(list_company[x][1]) > 0:
                if len(win) == 0:  # 全部錄取
                    break
                elif int(list_company[x][1]) == 0:  # 餘額規0
                    break
                else:
                    # !!待更改成資料庫直接修改!!
                    leave = int(list_company[x][1]) - 1
                    list_company[x][1] = leave
                    re_list = []
                    re_list.append(win[0][0])
                    re_list.append(win[0][1])
                    list_lu.append(re_list)  # 備取率取
                    for re in list_student_sort_two:
                        if re[0] == win[0][1]:
                            list_student_sort_two.remove(re)
                    win.remove(win[0])
                    # !!待更改成資料庫直接修改!!
        if len(list_student_sort_two) == front_sort_len:
            break
    # 存入資料庫中
    for unit in list_lu:
        student_ob = Student.objects.get(name=unit[1])
        company_ob = Company.objects.get(name=unit[0])
        check_result = Result.objects.filter(student=student_ob)  # 雙重驗證(可有可無)
        if not (check_result.exists()):
            Result.objects.create(student=student_ob, company=company_ob)


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
