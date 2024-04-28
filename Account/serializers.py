from rest_framework import serializers
from.models import Account

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user 