from django.db import models
from django.core import validators
from student.models import Student


class MonthReport(models.Model):

    title = models.CharField(max_length=10, verbose_name='標題', blank=True, null=True)
    student = models.ForeignKey(Student, related_name='diary_student', on_delete=models.CASCADE, verbose_name='學生')
    report = models.FileField(upload_to='report/', validators=[validators.FileExtensionValidator(['pdf'],
                              message='報告必須為pdf格式')], verbose_name='實習報告', blank=True, null=True)
    deadline = models.DateField(verbose_name='截止日期')
    delay_upload = models.BooleanField(verbose_name='補交', default=False)
    company_tutor_feedback = models.TextField(verbose_name='企業導師回饋', blank=True, null=True)
    company_tutor_feedback_date = models.DateField(verbose_name='企業導師回饋日期', blank=True, null=True)
    university_tutor_feedback = models.TextField(verbose_name='大學導師回饋', blank=True, null=True)
    university_tutor_feedback_date = models.DateField(verbose_name='大學導師回饋日期', blank=True, null=True)

    class Meta:
        ordering = ('student',)
        verbose_name = '實習報告'
        verbose_name_plural = '實習報告'

    def __str__(self):
        return self.student.user.username
