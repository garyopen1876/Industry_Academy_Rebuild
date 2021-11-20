from django.shortcuts import render, redirect
from .models import *
# from manager.models import Function
from web.models import Profile


# 媒合系統-企業頁面
def show_company(request):
    if request.user.profile.role == Profile.COMPANY:
        check_user = ContactPerson.objects.filter(user=request.user)
        check_upload = Function.objects.filter(function='新增職位資訊')
        check_resume = Function.objects.filter(function='履歷審察')
        check_admission = Function.objects.filter(function='正備取結果')
        check_result = Function.objects.filter(function='企業放榜結果')
    else:
        message = '身分錯誤！請先登出切換身分！'
        return redirect('/system')
    return render(request, 'company.html', locals())


# 企業-企業資訊
def company_information(request, company_id=None):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.COMPANY:
            check_user = ContactPerson.objects.filter(user=request.user)
            if check_user.exists():
                check_company = Company.objects.filter(contact_persons=check_user.get())
                if check_company.exists():
                    unit = check_company.get()
                else:
                    message = '企業資料未定義!'
                    return redirect('/system/company/companyEdit')
            else:
                message = '無此負責人!'
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'company_information.html', locals())
    else:
        return redirect('')


# 企業-編輯企業資訊
def company_edit(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.COMPANY:
            message = '請填入企業資料！'
            check_user = ContactPerson.objects.filter(user=request.user)
            if check_user.exists():
                check_company = Company.objects.filter(contact_persons=check_user.get())
                # 存在時顯示舊資料
                if check_company.exists():
                    unit = check_company.get()

                if request.method == 'POST':
                    if check_company.exists():
                        unit.name = request.POST['name']
                        unit.industry = request.POST['industry']
                        unit.uniform_numbers = request.POST['uniformNumbers']
                        unit.capital = request.POST['capital']
                        unit.employee = request.POST['employee']
                        unit.website = request.POST['website']
                        unit.address = request.POST['address']
                        unit.foreign = request.POST['foreign']
                        unit.inter_ship_start = request.POST['start']
                        unit.inter_ship_end = request.POST['end']
                        unit.work_time = request.POST['workTime']
                        unit.work_place = request.POST['workPlace']
                        unit.salary = request.POST['salary']
                        unit.welfare = request.POST['welfare']
                        unit.interview = request.POST['interview']
                        if request.FILES.get('introduction') is not None:
                            introduction = request.FILES.get('introduction')
                            if introduction.content_type.split('/')[1] != 'pdf':
                                message = '上傳格式錯誤！格式必須為 pdf 檔！'
                            else:
                                unit.introduction.delete()
                                unit.introduction = introduction
                                unit.save()
                                message = '修改資料成功！'
                        else:
                            # 沒有上傳檔案時
                            unit.save()
                            message = '修改資料成功！'
                    else:
                        c_name = request.POST['name']
                        c_industry = request.POST['industry']
                        c_uniform_numbers = request.POST['uniformNumbers']
                        c_capital = request.POST['capital']
                        c_employee = request.POST['employee']
                        c_website = request.POST['website']
                        c_address = request.POST['address']
                        c_foreign = request.POST['foreign']
                        c_start = request.POST['start']
                        c_end = request.POST['end']
                        c_work_time = request.POST['workTime']
                        c_work_place = request.POST['workPlace']
                        c_salary = request.POST['salary']
                        c_welfare = request.POST['welfare']
                        c_interview = request.POST['interview']
                        if request.FILES.get('introduction') is not None:
                            introduction = request.FILES.get('introduction')
                            if introduction.content_type.split('/')[1] != 'pdf':
                                message = '上傳格式錯誤！格式必須為 pdf 檔！'
                            else:
                                unit = Company.objects.create(contact_persons=check_user.get(),
                                                              name=c_name, industry=c_industry,
                                                              uniform_numbers=c_uniform_numbers, capital=c_capital,
                                                              employee=c_employee, website=c_website, address=c_address,
                                                              foreign=c_foreign, inter_ship_start=c_start,
                                                              inter_ship_end=c_end, work_time=c_work_time,
                                                              work_place=c_work_place, salary=c_salary,
                                                              welfare=c_welfare,
                                                              interview=c_interview)
                                unit.introduction = introduction
                                unit.save()
                                message = '資料上傳成功！'
                        else:
                            # 沒有上傳簡章時
                            unit = Company.objects.create(contact_persons=check_user.get(),
                                                          name=c_name, industry=c_industry,
                                                          uniform_numbers=c_uniform_numbers, capital=c_capital,
                                                          employee=c_employee, website=c_website, address=c_address,
                                                          foreign=c_foreign, inter_ship_start=c_start,
                                                          inter_ship_end=c_end, work_time=c_work_time,
                                                          work_place=c_work_place, salary=c_salary, welfare=c_welfare)
                            message = '資料上傳成功！'
            else:
                message = '無此負責人'
                return redirect('/system')
        else:
            message = '身分錯誤！請先登出切換身分！'
            return redirect('/system')
        return render(request, 'company_edit.html', locals())
    else:
        return redirect('')


# 企業-新增職位資訊
def company_upload(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.COMPANY and Function.objects.get(function='新增職位資訊').switch is True:
            check_user = ContactPerson.objects.filter(user=request.user)
            if check_user.exists():
                check_company = Company.objects.filter(contact_persons=check_user.get())
                if check_company.exists():
                    company_ob = check_company.get()
                    # 顯示職位內容
                    check_vacancy = VacancyRequirement.objects.filter(company=company_ob)
                    if check_vacancy.exists():
                        show_vacancy = check_vacancy
                    # post部分
                    if request.method == 'POST':
                        for unit in check_vacancy:
                            if unit.name in request.POST:
                                company_ob.vacancy = int(company_ob.vacancy) - int(unit.number)
                                company_ob.save()
                                unit.delete()
                                return redirect('/system/company/companyUpload')
                    else:
                        message = '請輸入資料'
                else:
                    message = '企業資料未定義!'
                    return redirect('/system/company/companyEdit')
            else:
                message = '無此負責人'
                return redirect('/system')
        else:
            message = '身分錯誤！請先登出切換身分 or 功能尚未開放！'
            return redirect('/system')
        return render(request, 'company_upload.html', locals())
    else:
        return redirect('')


# 企業-新增職位詳細內容
def company_vacancy_new(request):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.COMPANY and Function.objects.get(function='新增職位資訊').switch is True:
            check_user = ContactPerson.objects.filter(user=request.user)
            if check_user.exists():
                check_company = Company.objects.filter(contact_persons=check_user.get())
                if check_company.exists():
                    unit = check_company.get()
                    if request.method == 'POST':
                        vacancy_name = request.POST['vacancyName']
                        vacancy_required_skill = request.POST['vacancyRequiredSkill']
                        vacancy_content = request.POST['vacancyContent']
                        vacancy_number = request.POST['vacancyNumber']
                        VacancyRequirement.objects.create(company=unit, name=vacancy_name,
                                                          required_skill=vacancy_required_skill,
                                                          content=vacancy_content,
                                                          number=vacancy_number)
                        # 增加職位總數
                        unit.vacancy = int(unit.vacancy) + int(vacancy_number)
                        unit.save()
                        return redirect('/system/company/companyUpload')
                else:
                    message = '企業資料未定義!'
                    return redirect('/system/company/companyEdit')
            else:
                message = '無此負責人'
                return redirect('/system')
        else:
            message = '身分錯誤！請先登出切換身分 or 功能尚未開放！'
            return redirect('/system')
        return render(request, 'company_vacancy_new.html', locals())
    else:
        return redirect('')


# 企業-編輯職位詳細內容
def company_vacancy_edit(request, company_vacancy_edit_id=None):
    if request.user.is_authenticated:
        if request.user.profile.role == Profile.COMPANY and Function.objects.get(function='新增職位資訊').switch is True:
            check_user = ContactPerson.objects.filter(user=request.user)
            if check_user.exists():
                check_company = Company.objects.filter(contact_persons=check_user.get())
                if check_company.exists():
                    company_ob = check_company.get()
                    unit = VacancyRequirement.objects.get(id=company_vacancy_edit_id)
                    # 防他公司竄改
                    if unit.company != company_ob:
                        return redirect('/system/company')

                    if request.method == 'POST':
                        # 刪減原本的職位數
                        company_ob.vacancy = int(company_ob.vacancy) - int(unit.number)
                        unit.name = request.POST['vacancyName']
                        unit.required_skill = request.POST['vacancyRequiredSkill']
                        unit.content = request.POST['vacancyContent']
                        unit.number = request.POST['vacancyNumber']
                        # 改改職位總數
                        company_ob.vacancy = int(company_ob.vacancy) + int(unit.number)
                        unit.save()
                        company_ob.save()
                        return redirect('/system/company/companyUpload')
                else:
                    message = '企業資料未定義!'
                    return redirect('/system/company/companyEdit')
            else:
                message = '無此負責人'
                return redirect('/system')
        else:
            message = '身分錯誤！請先登出切換身分 or 功能尚未開放！'
            return redirect('/system')
        return render(request, 'company_vacancy_edit.html', locals())
    else:
        return redirect('')
