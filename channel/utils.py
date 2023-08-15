from django.db import transaction
from django.db.models import F

from channel.models import Share


@transaction.atomic
def buy(buyer, channel_id, price):
    buyer.wallet.balance = F('balance') - price
    buyer.wallet.save()
    total = 0
    for share in Share.objects.filter(channel_id=channel_id):
        total += share.amount
    for share in Share.objects.filter(channel_id=channel_id).select_related('owner__wallet'):
        share.owner.wallet.balance = F('balance') + share.amount * price / total
        share.owner.wallet.save()
