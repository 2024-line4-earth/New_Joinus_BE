from django.db import migrations

def remove_invalid_sharedcards(apps, schema_editor):
    SharedCard = apps.get_model("share", "SharedCard")

    # FK 로 cardpost를 따라가고, cardpost.user와 shared_card.user가 서로 다른 경우 제거
    for shared_card in SharedCard.objects.select_related("cardpost"):
        if shared_card.user_id != shared_card.cardpost.user_id:
            shared_card.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('join', '0003_alter_cardpost_keyword'), 
        ('share', '0003_alter_sharedcard_cardpost'), 
    ]

    operations = [
        migrations.RunPython(remove_invalid_sharedcards),
    ]
    