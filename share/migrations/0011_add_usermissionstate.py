from django.db import migrations
import random

KEYWORD_CHOICES = [
    "STANDBY_POWER",
    "RECYCLING",
    "SAVING",
    "SEPARATION",
    "REUSABLE",
    "ECO_FRIENDLY",
    "TUMBLER",
    "CAMPAIGN",
    "OTHER",
]

def create_mission_state_for_existing_users(apps, schema_editor):
    User = apps.get_model("users", "User")
    UserMissionState = apps.get_model("share", "UserMissionState")
    CardMission = apps.get_model("share", "CardMission")

    for user in User.objects.all():
        if not UserMissionState.objects.filter(user=user).exists():
            state = UserMissionState.objects.create(user=user)
            keyword = random.choice(KEYWORD_CHOICES)
            CardMission.objects.create(mission_state=state, keyword=keyword)

class Migration(migrations.Migration):

    dependencies = [
        ("share", "0010_usermissionstate_cardmission"),
        ("users", "0004_user_current_theme"),
    ]

    operations = [
        migrations.RunPython(create_mission_state_for_existing_users),
    ]
