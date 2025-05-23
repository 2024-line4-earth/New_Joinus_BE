# Generated by Django 5.1.7 on 2025-05-07 17:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('join', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(help_text='추가 설명')),
                ('is_finalized', models.BooleanField(default=False, help_text='보관상태(공유중단상태) 여부')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cardpost', models.ForeignKey(help_text='원본 카드', on_delete=django.db.models.deletion.CASCADE, related_name='shared_cards', to='join.cardpost')),
                ('user', models.ForeignKey(help_text='공유한 사용자', on_delete=django.db.models.deletion.CASCADE, related_name='shared_cards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'share_sharedcard',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='share_comments', to=settings.AUTH_USER_MODEL)),
                ('sharedcard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='share.sharedcard')),
            ],
            options={
                'db_table': 'share_comment',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='CardReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_reports', to=settings.AUTH_USER_MODEL)),
                ('sharedcard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='share.sharedcard')),
            ],
            options={
                'db_table': 'share_cardreport',
            },
        ),
        migrations.CreateModel(
            name='CardLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_likes', to=settings.AUTH_USER_MODEL)),
                ('sharedcard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='share.sharedcard')),
            ],
            options={
                'db_table': 'share_cardlike',
                'unique_together': {('user', 'sharedcard')},
            },
        ),
    ]
