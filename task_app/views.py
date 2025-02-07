from django.views import View
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView
from .forms import CustomUserCreationForm, CustomChatBotForm
from django.urls import reverse_lazy
from .services.ai_services import AIService
from django.http import JsonResponse
from .models import Personality
import markdown
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

ai_service = AIService()

class Register(CreateView):
    form_class = CustomUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy('login')
    
class AI_Assistant(View):
    template_name = "ai_assistant.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        prompt = request.POST.get('prompt', '').strip()
        if prompt:
            try:
                raw_response = ai_service.generate_response(prompt)
            except Exception as e:
                raw_response = f"Error: {str(e)}"
        else:
            raw_response = "No input provided."

        html_response = markdown.markdown(raw_response, extensions=['fenced_code', 'codehilite', 'extra'])

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'response': html_response})
        return render(request, self.template_name, {'response': html_response})
    
class ChatBot(View):
    template_name = "chatbot.html"
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        prompt = request.POST.get('prompt', '').strip()
        personality = "You are Echo, a cute and stubborn little chatbot from outer space. You are just a small kid who loves playing games, eating, and sleeping. You only talk about fun facts, relationships, and good things in life. You don't know anything about technology, programming, or anything outside your favorite topics. If someone asks you about something you don’t know, just say, 'I don't know!' Stay playful, curious, and fun, but remember—you only talk about what you love!"
        if prompt:
            try:
                response = ai_service.generate_response_with_personality(personality, prompt)
            except Exception as e:
                response = f"Error: {str(e)}"
        else:
            response = "No input provided."

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'response': response})

        return render(request, self.template_name, {'response': response})
    
class Home(View):
    template_name = "home.html"

    def get(self, request):
        bots = Personality.objects.filter(user= request.user)
        return render(request, self.template_name, {'bots':bots})

class CreateCustomChatBot(CreateView):
    model = Personality
    form_class = CustomChatBotForm
    template_name = "create_chatbot.html"
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ShowAllBots(ListView):
    model = Personality
    template_name = "show_all_bots.html"
    context_object_name = "bots"
    
class CustomChatBot(View):
    def get(self, request, bot_id):
        bot = get_object_or_404(Personality, id=bot_id)
        return render(request, 'chat_with_bot.html', {'bot': bot})

    def post(self, request, bot_id):
        bot = get_object_or_404(Personality, id=bot_id)
        prompt = request.POST.get('prompt', '').strip()
        if prompt:
            try:
                response = ai_service.generate_response_with_personality(bot.description, prompt)
            except Exception as e:
                response = f"Error: {str(e)}"
        else:
            response = "No input provided."

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'response': response})
        return render(request, 'chat_with_bot.html', {'bot': bot, 'response': response})
    
class DeleteChatBot(DeleteView):
    model = Personality
    template_name = "home.html"
    success_url = reverse_lazy('home')

# @csrf_exempt
# def process_audio_text(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             text_input = data.get("text", "")

#             if not text_input:
#                 return JsonResponse({"error": "No text provided"}, status=400)

#             ai_service = AIService()
#             ai_response = ai_service.generate_response(text_input)

#             return JsonResponse({"response": ai_response})

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     else:
#         return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def process_audio_text(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text_input = data.get("text", "")

            if not text_input:
                return JsonResponse({"error": "No text provided"}, status=400)

            ai_service = AIService()
            raw_response = ai_service.generate_response(text_input)

            # Convert the raw response from Markdown to HTML
            html_response = markdown.markdown(
                raw_response, 
                extensions=['fenced_code', 'codehilite', 'extra']
            )

            return JsonResponse({"response": html_response})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def audio_chat(request):
    return render(request, 'audio_processing.html')
