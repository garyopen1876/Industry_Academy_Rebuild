from django.db import models
from django.contrib.auth.models import User
from django.core import validators


class Profile(models.Model):
    STUDENT = 1
    COMPANY = 2
    MANAGER = 3
    UNIVERSITY_TUTOR = 4
    COMPANY_TUTOR1 = 5
    COMPANY_TUTOR2 = 6

    ROLE_CHOICES = (
        (STUDENT, '學生'),
        (COMPANY, '企業-人資'),
        (MANAGER, '管理者'),
        (UNIVERSITY_TUTOR, '大學-實習導師'),
        (COMPANY_TUTOR1, '企業-實習導師1'),
        (COMPANY_TUTOR2, '企業-實習導師2'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    title = models.CharField(max_length=10, verbose_name='標題', blank=True)
    content = models.TextField(verbose_name='內容', blank=True)
    created = models.DateTimeField(auto_created=True, verbose_name='發布時間')
    url = models.FileField(upload_to='message/', validators=[validators.FileExtensionValidator(['pdf'],
                           message='簡介必須為pdf格式')], verbose_name='檔案附件', blank=True, null=True)

    class Meta:
        ordering = ('created',)
        verbose_name = '公佈欄'
        verbose_name_plural = '公佈欄'

    def __str__(self):
        return self.title
