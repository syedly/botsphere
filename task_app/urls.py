from django.urls import path
from .views import AI_Assistant, Register, ChatBot, Home, CreateCustomChatBot, ShowAllBots, CustomChatBot, DeleteChatBot, audio_chat, process_audio_text
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', Register.as_view(), name="register"),
    path('ai_assistant/', AI_Assistant.as_view(), name="ai_assistant"),
    path('chatbot/', ChatBot.as_view(), name="chatbot"),
    path('home/', Home.as_view(), name="home"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('create_chatbot/', CreateCustomChatBot.as_view(), name="create_chatbot"),
    path('show_all_bots/', ShowAllBots.as_view(), name="show_all_bots"),
    path('chat/<int:bot_id>/', CustomChatBot.as_view(), name='chat_with_bot'),
    path('delete-chat-bot/<int:pk>/', DeleteChatBot.as_view(), name='delete-chat-bot'),
    path('audio_processing/', audio_chat, name='audio_processing'),
    path('api/process_audio_text/', process_audio_text, name="process_audio_text"),
]