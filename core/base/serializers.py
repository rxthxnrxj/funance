from rest_framework import serializers
from .models import User, Intriguer, UserIntriguerInteraction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'age', 'points', 'current_streak',
                  'longest_streak', 'last_interaction', 'last_intriguer_shown', 'location']


class IntriguerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intriguer
        fields = ['id', 'text', 'theme', 'amount', 'chunk',
                  'date_added', 'times_shown', 'last_shown', 'thumbnail']


class UserIntriguerInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIntriguerInteraction
        fields = ['id', 'user', 'intriguer', 'shown_at', 'responded', 'liked']
