from rest_framework import serializers
from logic.models import Auction

class myserializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('auction', 'title', 'desc','min_price','deadline','createdAt','modifiedAt','authName','tala','is_banned','seller_id','is_locked')
