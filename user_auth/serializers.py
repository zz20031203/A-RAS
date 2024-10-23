from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'tel', 'role', 'doctor_license', 'doctor_name']
        extra_kwargs = {
            'doctor_license': {'required': False},
            'doctor_name': {'required': False}
        }


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=128)
    repassword = serializers.CharField(max_length=128)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    doctor_license = serializers.CharField(max_length=50, allow_blank=True, required=False)
    doctor_name = serializers.CharField(max_length=100, allow_blank=True, required=False)

    def validate(self, data):
        if data['password'] != data['repassword']:
            raise serializers.ValidationError({"repassword": "Passwords must match."})

        # 如果角色是医生，检查医师证号和姓名是否存在
        if data['role'] == 'doctor':
            if not data.get('doctor_license') or not data.get('doctor_name'):
                raise serializers.ValidationError("Doctor's license and name are required for doctor registration.")

        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = UserProfile.objects.create_user(
            username=validated_data['phone'],  # 假设用户名为电话号码
            password=validated_data['password'],
            tel=validated_data['phone'],
            role=role
        )
        if role == 'doctor':
            user.doctor_license = validated_data.get('doctor_license', '')
            user.doctor_name = validated_data.get('doctor_name', '')
            user.save()
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=128)
