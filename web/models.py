from django.db import models
from django.contrib.auth.models import User


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
