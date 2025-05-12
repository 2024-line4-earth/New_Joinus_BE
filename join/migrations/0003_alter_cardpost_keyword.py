from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('join', '0002_add_keyword_and_migrate_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardpost',
            name='keywords',
        ),
        migrations.AlterField(
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
                null=False,
            ),
        )
    ]