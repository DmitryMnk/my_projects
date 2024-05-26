from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'email', 'password1', 'password2', 'first_name', 'last_name'
        extra_kwargs = {
            'password1': {'write_only': True}
        }

    def validate_email(self):
        mail = self.validated_data['email'].strip().loswer()
        if User.objects.filter(email=mail).exists():
            return False
        return True
