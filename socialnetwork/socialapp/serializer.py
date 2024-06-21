from rest_framework import serializers
from .models import User, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name')



class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password','name')
        extra_kwrgs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', '')
        )
        
        return user
    


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'status', 'created_at')
        read_only_fields = ('id', 'created_at')



class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name')


class PendingFriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'status', 'created_at')

    def get_from_user(self, obj):
        return {
            'id': obj.from_user.id,
            'email': obj.from_user.email,
            'name': obj.from_user.name,
        }