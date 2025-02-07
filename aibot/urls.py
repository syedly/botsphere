from django.urls import path
from . views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('Login/', LoginView.as_view(), name='Login'),
    path('showallbots/', ShowAllBots.as_view(), name='showallbots'),
    path('customizebot/', CustomizeBotView.as_view(), name='customizebot'),
    path('deletebot/<int:pk>/', DeleteBot.as_view(), name='deletebot'),
    path('chatwithbot/<int:bot_id>/', ChatWithBot.as_view(), name='chatwithbot'),
]
