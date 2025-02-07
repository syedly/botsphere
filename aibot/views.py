from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import*
from rest_framework.permissions import IsAuthenticated
from task_app.services.ai_services import AIService

ai_service = AIService()
# Create your views here.

class SignupView(generics.CreateAPIView):
    query_set = User.objects.all()
    serializer_class = SignupSerializer
    
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            "message": "login successfully!"
        })
        
class ShowAllBots(generics.ListAPIView):
    serializer_class = CustomizeBotSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CustomizeBot.objects.all()
        
class CustomizeBotView(generics.ListCreateAPIView):
    serializer_class = CustomizeBotSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return CustomizeBot.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        


class ChatWithBot(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        bot_id = self.kwargs.get('bot_id')  # Get bot_id from URL
        bot = get_object_or_404(CustomizeBot, id=bot_id)  # Ensure 'bot' key exists

        message = serializer.validated_data.get('message')  # Get message from validated data
        response = ai_service.generate_response_with_personality(bot.personality, message)  # Generate AI response

        # Save chat with generated response
        serializer.save(user=user, bot=bot, response=response)
        
class DeleteBot(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomizeBotSerializer
    queryset = CustomizeBot.objects.all()
    
    def get_object(self):
        object = get_object_or_404(CustomizeBot, pk=self.kwargs.get('pk'))
        if object.user != self.request.user:
            raise PermissionError("You have no access to delete this bot")
        return object
    