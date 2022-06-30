# Generated by Django 4.0.5 on 2022-06-29 02:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5, verbose_name='이름')),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Painting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='제목')),
                ('descriptions', models.TextField(max_length=256, verbose_name='설명')),
                ('image', models.FileField(upload_to='auction/', verbose_name='이미지')),
                ('artist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='artist_painting', to=settings.AUTH_USER_MODEL, verbose_name='원작자')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auction.category', verbose_name='카테고리')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_painting', to=settings.AUTH_USER_MODEL, verbose_name='소유자')),
            ],
            options={
                'db_table': 'paintings',
            },
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_bid', models.PositiveIntegerField(verbose_name='시작 입찰가')),
                ('current_bid', models.PositiveIntegerField(null=True, verbose_name='현재 입찰가')),
                ('auction_start_date', models.DateTimeField(auto_now_add=True, verbose_name='경매 시작일')),
                ('auction_end_date', models.DateTimeField(verbose_name='경매 종료일')),
                ('bidder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('painting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.painting')),
            ],
            options={
                'db_table': 'auctions',
            },
        ),
    ]
