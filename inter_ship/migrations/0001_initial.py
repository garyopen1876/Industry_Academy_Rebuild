# Generated by Django 3.2.9 on 2021-11-21 12:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=10, null=True, verbose_name='標題')),
                ('report', models.FileField(blank=True, null=True, upload_to='report/', validators=[django.core.validators.FileExtensionValidator(['pdf'], message='報告必須為pdf格式')], verbose_name='實習報告')),
                ('deadline', models.DateField(verbose_name='截止日期')),
                ('delay_upload', models.BooleanField(default=False, verbose_name='補交')),
                ('company_tutor_feedback', models.TextField(blank=True, null=True, verbose_name='企業導師回饋')),
                ('company_tutor_feedback_date', models.DateField(blank=True, null=True, verbose_name='企業導師回饋日期')),
                ('university_tutor_feedback', models.TextField(blank=True, null=True, verbose_name='大學導師回饋')),
                ('university_tutor_feedback_date', models.DateField(blank=True, null=True, verbose_name='大學導師回饋日期')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diary_student', to='student.student', verbose_name='學生')),
            ],
            options={
                'verbose_name': '實習報告',
                'verbose_name_plural': '實習報告',
                'ordering': ('student',),
            },
        ),
    ]
