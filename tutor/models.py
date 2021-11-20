from django.db import models
from django.contrib.auth.models import User


class Tutor(models.Model):
    UNIVERSITY_TUTOR = 4
    COMPANY_TUTOR1 = 5
    COMPANY_TUTOR2 = 6
    TUTOR_ROLE = (
        (UNIVERSITY_TUTOR, '大學-實習導師'),
        (COMPANY_TUTOR1, '企業-實習導師1'),
        (COMPANY_TUTOR2, '企業-實習導師2'),
    )
    user = models.ForeignKey(User, related_name='tutor_user', on_delete=models.CASCADE, verbose_name='使用者')
    name = models.CharField(max_length=30, verbose_name='導師姓名', blank=True)
    phone = models.CharField(max_length=50, verbose_name='聯絡電話', blank=True)
    email = models.CharField(max_length=100, verbose_name='email', blank=True)
    category = models.PositiveSmallIntegerField(choices=TUTOR_ROLE, verbose_name='分類', blank=True)

    class Meta:
        ordering = ('user',)
        verbose_name = '實習導師'
        verbose_name_plural = '實習導師'

    def __str__(self):
        return self.name
