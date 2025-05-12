from django.db import models
from django.conf import settings

class PinnedSharedCard(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pinned_cards"
    )
    shared_card = models.OneToOneField( 
        "share.SharedCard",
        on_delete=models.CASCADE,
        related_name="pinned_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "share_pinnedsharedcard"
        unique_together = ("user", "shared_card")  

    def __str__(self):
        return f"{self.user_id} pinned {self.shared_card_id}"
