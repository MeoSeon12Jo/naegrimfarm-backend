# Generated by Django 4.0.5 on 2022-07-04 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='이메일')),
                ('nickname', models.CharField(max_length=15, unique=True, verbose_name='닉네임')),
                ('password', models.CharField(max_length=256, verbose_name='비밀번호')),
                ('point', models.PositiveIntegerField(default=3000000, verbose_name='포인트')),
                ('is_active', models.BooleanField(default=True, verbose_name='계정 활성화 여부')),
                ('is_admin', models.BooleanField(default=False, verbose_name='관리자 권한')),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
