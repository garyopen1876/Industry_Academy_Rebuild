from django.db import models
from django.contrib.auth.models import User
from django.core import validators


class ContactPerson(models.Model):
    user = models.ForeignKey(User, related_name='company_user', on_delete=models.CASCADE, verbose_name='使用者',
                             blank=True, null=True)
    name = models.CharField(max_length=50, verbose_name='姓名', blank=True)
    phone = models.CharField(max_length=50, verbose_name='聯絡電話', blank=True)
    email = models.CharField(max_length=100, verbose_name='email', blank=True)

    class Meta:
        ordering = ('user',)
        verbose_name = '企業聯絡人'
        verbose_name_plural = '企業聯絡人'

    def __str__(self):
        return self.name


class Company(models.Model):
    contact_persons = models.ManyToManyField(ContactPerson, verbose_name='企業聯絡人', blank=True)
    name = models.CharField(max_length=30, verbose_name='公司名稱', blank=True)
    industry = models.CharField(max_length=100, verbose_name='產業別', blank=True)
    uniform_numbers = models.CharField(max_length=20, verbose_name='統一編號', blank=True)
    capital = models.CharField(max_length=50, verbose_name='資本額', blank=True)
    employee = models.IntegerField(verbose_name='員工數', blank=True, default=0)
    website = models.CharField(max_length=100, verbose_name='公司網站', blank=True)
    address = models.CharField(max_length=100, verbose_name='通訊地址', blank=True)
    foreign = models.CharField(max_length=10, verbose_name='是否接受外籍生實習', blank=True)
    inter_ship_start = models.CharField(max_length=15, verbose_name='實習期間 (起)', blank=True)
    inter_ship_end = models.CharField(max_length=15, verbose_name='實習期間 (訖)', blank=True)
    work_time = models.CharField(max_length=30, verbose_name='工作時間', blank=True)
    work_place = models.TextField(verbose_name='實習地點地址', blank=True)
    vacancy = models.IntegerField(verbose_name='實習名額', blank=True, default=0)
    salary = models.TextField(verbose_name='薪資', blank=True)
    welfare = models.CharField(max_length=20, verbose_name='其他福利', blank=True)
    explanation = models.CharField(max_length=500, verbose_name='廠商說明會日期', blank=True)
    introduction = models.FileField(upload_to='company/', validators=[validators.FileExtensionValidator(['pdf'],
                                    message='簡介必須為pdf格式')], verbose_name='簡介', blank=True, null=True)
    interview = models.CharField(max_length=50, verbose_name='面試方式', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = '企業資料'
        verbose_name_plural = '企業資料'

    def __str__(self):
        return self.name


class VacancyRequirement(models.Model):
    company = models.ForeignKey(Company, related_name='vacancyRequirement_company', on_delete=models.CASCADE,
                                verbose_name='公司')
    name = models.CharField(max_length=20, verbose_name='職位名稱', blank=True, null=True)
    required_skill = models.TextField(verbose_name='所需專長', blank=True)
    number = models.IntegerField(verbose_name='職位名額', blank=True, default=0)
    content = models.TextField(verbose_name='職位內容', blank=True)

    class Meta:
        ordering = ('company',)
        verbose_name = '職缺資料'
        verbose_name_plural = '職缺資料'

    def __str__(self):
        return self.name

