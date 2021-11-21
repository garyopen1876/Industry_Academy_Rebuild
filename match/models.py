from django.db import models
from company.models import Company
from student.models import Student


class Admission(models.Model):
    company = models.ForeignKey(Company, related_name='admission_company', on_delete=models.CASCADE, verbose_name='公司')
    student = models.ForeignKey(Student, related_name='admission_student', on_delete=models.CASCADE, verbose_name='學生')
    volunteer_order = models.CharField(max_length=10, verbose_name='志願序', blank=True, null=True)
    sort = models.CharField(max_length=10, verbose_name='正備取')
    vacancy = models.CharField(max_length=100, verbose_name='應徵職位')
    vacancy_result = models.CharField(max_length=20, verbose_name='錄取職位', blank=True, null=True)
    review = models.CharField(max_length=50, verbose_name='履歷審查結果', blank=True, null=True, default='履歷尚未審閱')
    feedback = models.TextField(verbose_name='履歷審查回饋', blank=True, null=True)
    remark = models.TextField(verbose_name='備註', blank=True)

    class Meta:
        ordering = ('student',)
        verbose_name = '媒合資訊'
        verbose_name_plural = '媒合資訊'


class Result(models.Model):
    student = models.ForeignKey(Student, related_name='result_student', on_delete=models.CASCADE, verbose_name='學生')
    company = models.ForeignKey(Company, related_name='result_company', on_delete=models.CASCADE, verbose_name='公司')
    result_vacancy = models.CharField(max_length=20, verbose_name='獲得職位')

    class Meta:
        ordering = ('student',)
        verbose_name = '媒合結果'
        verbose_name_plural = '媒合結果'
