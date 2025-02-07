from rest_framework import serializers
from django.contrib.auth.models import User
from .models import*
from django.contrib.auth import authenticate
from task_app.services.ai_services import AIService

ai_service = AIService()

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}  
        }

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username is already taken!')
        
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')  
        user = User(**validated_data)  
        user.set_password(password)  
        user.save()  
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        
        data['user'] = user
        return data
    
class CustomizeBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomizeBot
        fields = ['id', 'name', 'personality']
        
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['message', 'response', 'bot']  # Ensure 'bot' is included in the output
        read_only_fields = ['response']  # Make response read-only so it can't be provided manually

    def create(self, validated_data):
        bot = validated_data['bot']
        message = validated_data['message']
        user = self.context['request'].user

        # Generate response using AI service
        response = ai_service.generate_response_with_personality(bot.personality, message)

        # Save the chat object with the generated response
        chat = Chat.objects.create(user=user, bot=bot, message=message, response=response)
        return chat
