from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from company.models import Company
from tutor.models import Tutor
import os
import uuid


# 加入uuid讓檔案更安全
def rename(instance, filename):
    name = filename.split('.')[0]
    random = uuid.uuid4()
    return os.path.join('student/{0}{1}.pdf'.format(name, random))


class Student(models.Model):
    user = models.ForeignKey(User, related_name='student_user', on_delete=models.CASCADE, verbose_name='使用者')
    name = models.CharField(max_length=10, verbose_name='姓名', blank=True)
    class_name = models.CharField(max_length=10, verbose_name='班級', blank=True)
    phone = models.CharField(max_length=50, verbose_name='聯絡電話', blank=True)
    email = models.CharField(max_length=100, verbose_name='email', blank=True)
    give_up = models.BooleanField(verbose_name='放棄名額', default=False)

    class Meta:
        ordering = ('user',)
        verbose_name = '學生資料'
        verbose_name_plural = '學生資料'

    def __str__(self):
        return self.user.username


class Resume(models.Model):
    student = models.ForeignKey(Student, related_name='resume_student', on_delete=models.CASCADE,  verbose_name='學生',
                                blank=True)
    company = models.ManyToManyField(Company, verbose_name='投履的公司', blank=True)
    resume = models.FileField(upload_to=rename, validators=[validators.FileExtensionValidator(['pdf'],
                              message='履歷必須為pdf格式')], verbose_name='履歷', blank=True, null=True)

    class Meta:
        ordering = ('student',)
        verbose_name = '學生履歷'
        verbose_name_plural = '學生履歷'

    def get_company(self):
        return "；".join([str(n) for n in self.company.all()])

    def __str__(self):
        return self.student.user.username


class InterShip(models.Model):
    student = models.ForeignKey(Student, related_name='inter_ship_student', on_delete=models.CASCADE, verbose_name='學生')
    company = models.ForeignKey(Company, related_name='inter_ship_company', on_delete=models.CASCADE, verbose_name='公司')
    vacancy = models.CharField(max_length=20, verbose_name='實習職位', blank=True)
    start = models.DateField(verbose_name='實習期間 (起)', blank=True)
    end = models.DateField(verbose_name='實習期間 (訖)', blank=True)
    company_tutor1 = models.ForeignKey(Tutor, related_name='inter_ship_company_tutor1', on_delete=models.CASCADE,
                                       verbose_name='企業-實習導師1', blank=True, null=True)
    company_tutor2 = models.ForeignKey(Tutor, related_name='inter_ship_company_tutor2', on_delete=models.CASCADE,
                                       verbose_name='企業-實習導師2', blank=True, null=True)
    university_tutor = models.ForeignKey(Tutor, related_name='inter_ship_university_tutor',
                                         on_delete=models.CASCADE, verbose_name='大學-實習導師', blank=True, null=True)

    class Meta:
        ordering = ('student',)
        verbose_name = '實習資料'
        verbose_name_plural = '實習資料'

    def __str__(self):
        return self.student.user.username
