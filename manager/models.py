from django.db import models


class Function(models.Model):
    role = models.CharField(max_length=20, verbose_name='功能身分')
    function = models.CharField(max_length=20, verbose_name='功能名稱')
    switch = models.BooleanField(default=False, verbose_name='開關狀態')

    class Meta:
        ordering = ('function',)
        verbose_name = '功能開關'
        verbose_name_plural = '功能開關'
