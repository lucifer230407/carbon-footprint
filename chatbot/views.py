import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import ChatMessage


class OpenRouterChatbot:
    """Simple chatbot using OpenRouter API"""
    
    def __init__(self, api_key, model=None):
        self.api_key = api_key
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = model or getattr(settings, 'OPENROUTER_MODEL', "openai/gpt-3.5-turbo")
    
    def chat(self, message):
        """Send a message and get response"""
        try:
            if not self.api_key or self.api_key == 'sk-or-v1-default-key':
                return "Error: OpenRouter API key not configured. Please set OPENROUTER_API_KEY in config_secret.py or environment variables."
            
            response = requests.post(
                url=self.url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "https://carbon-tracker.local",
                    "X-Title": "Carbon Footprint Chatbot",
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": message}]
                },
                timeout=30
            )
            
            if response.status_code == 401:
                return "Error: Invalid API key. Please check your OpenRouter API key in config_secret.py"
            
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return "Error: Connection error. Please check your internet connection."
        except Exception as e:
            return f"Error: {str(e)}"


@login_required
def chatbot_page(request):
    """Display the chatbot page"""
    return render(request, 'chatbot/index.html')


@login_required
@require_http_methods(["POST"])
def chat_api(request):
    """API endpoint for chatbot messages"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Get API key from settings
        api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
        if not api_key:
            return JsonResponse({'error': 'API key not configured'}, status=500)
        
        # Initialize chatbot and get response
        bot = OpenRouterChatbot(api_key)
        bot_response = bot.chat(user_message)
        
        # Save to database if user is authenticated
        if request.user.is_authenticated:
            ChatMessage.objects.create(
                user=request.user,
                user_message=user_message,
                bot_response=bot_response
            )
        
        return JsonResponse({
            'success': True,
            'response': bot_response
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
