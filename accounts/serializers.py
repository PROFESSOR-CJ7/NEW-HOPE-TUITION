from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

Parent = get_user_model()  # Fungua na funga bracket hapa

class ParentSignupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    language_preference = serializers.ChoiceField(
        choices=[('sw', 'Swahili'), ('en', 'English')],
        default='sw'
    )
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Parent
        fields = ('phone_number', 'name', 'language_preference', 'password')

    def create(self, validated_data):
        return Parent.objects.create_user(
            phone_number=validated_data['phone_number'],
            name=validated_data['name'],
            language_preference=validated_data['language_preference'],
            password=validated_data['password']
        )

class ParentLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password     = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = attrs.get('phone_number')
        pwd   = attrs.get('password')
        user  = authenticate(username=phone, password=pwd)
        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid phone number or password")
        attrs['user'] = user
        return attrs
