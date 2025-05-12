from django.db import migrations, models

def migrate_keywords_to_keyword(apps, schema_editor):
    CardPost = apps.get_model("join", "CardPost")
    for post in CardPost.objects.all():
        if post.keywords:
            post.keyword = post.keywords[0]
            post.save()

class Migration(migrations.Migration):

    dependencies = [
        ('join', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardpost',
            name='keyword',
            field=models.CharField(
                choices=[
                    ('STANDBY_POWER', '대기전력'),
                    ('RECYCLING', '재활용'),
                    ('SAVING', '물절약'),
                    ('SEPARATION', '분리배출'),
                    ('REUSABLE', '다회용기'),
                    ('ECO_FRIENDLY', '친환경'),
                    ('TUMBLER', '텀블러'),
                    ('CAMPAIGN', '캠페인'),
                    ('OTHER', '기타'),
                ],
                max_length=20,
                null=True,  
            ),
        ),

        migrations.RunPython(migrate_keywords_to_keyword),
    ]