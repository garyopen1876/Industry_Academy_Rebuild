from django.db import models
from django.core import validators


class Function(models.Model):
    role = models.CharField(max_length=20, verbose_name='功能身分')
    function = models.CharField(max_length=20, verbose_name='功能名稱')
    switch = models.BooleanField(default=False, verbose_name='開關狀態')

    class Meta:
        ordering = ('function',)
        verbose_name = '功能開關'
        verbose_name_plural = '功能開關'


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
