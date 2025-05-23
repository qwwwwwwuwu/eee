from rest_framework import serializers
from .models import Ad, ExchangeProposal
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AdSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ['created_at']


class ExchangeProposalSerializer(serializers.ModelSerializer):
    ad_sender = AdSerializer(read_only=True)
    ad_receiver = AdSerializer(read_only=True)
    
    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ['created_at', 'status']