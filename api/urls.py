from django.urls import path, include

urlpatterns = [
    path('aibot/', include('aibot.urls')),
]
