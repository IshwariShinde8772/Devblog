
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import requests

from blogs.models import Blog, Category
from assignments.models import About
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

def home(request):
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('-updated_at')
    posts = Blog.objects.filter(status='Published').order_by('-updated_at')
    
    # Fetch about us
    try:
        about = About.objects.get()
    except:
        about = None
    context = {
        'featured_posts': featured_posts,
        'posts': posts,
        'about': about,
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            # authentication failed unexpectedly; fall through to re-render form with errors
    form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')


@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """
    API endpoint for chatbot that uses OpenRouter API.
    Make sure to set OPENROUTER_API_KEY in Django settings.
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        print(f"\n[ChatBot API] Received message: {user_message}")
        
        # Get blog context for the chatbot
        blog_context = get_blog_context()
        
        # Prepare the system prompt
        system_prompt = f"""You are a helpful blog assistant for DevBlog platform. You provide recommendations and answer questions about blog posts and categories.

Current Blog Statistics:
{blog_context}

When answering:
1. Be friendly and conversational
2. Provide specific blog recommendations if relevant
3. Help users find content in their categories of interest
4. Keep responses concise (under 150 words)
5. Always encourage users to explore the full articles on the platform"""

        # Call OpenRouter API
        print(f"[ChatBot API] Getting response from OpenRouter...")
        reply = call_openrouter_api(user_message, system_prompt)
        print(f"[ChatBot API] Got reply: {reply[:100]}...")
        
        return JsonResponse({
            'reply': reply,
            'status': 'success'
        })
    
    except json.JSONDecodeError:
        print(f"[ChatBot API] JSON Decode Error")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"[ChatBot API] Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


def get_blog_context():
    """Gather context about available blogs and categories"""
    try:
        total_posts = Blog.objects.filter(status='Published').count()
        categories = Category.objects.all().count()
        recent_posts = Blog.objects.filter(status='Published').order_by('-created_at')[:5]
        
        context = f"""
- Total Published Posts: {total_posts}
- Total Categories: {categories}

Recent Posts:
"""
        for post in recent_posts:
            context += f"  • {post.title} (by {post.author.username}) - Category: {post.category.category_name}\n"
        
        return context
    except:
        return "- Unable to fetch blog statistics"


def call_openrouter_api(user_message, system_prompt):
    """
    Call OpenRouter API to get chatbot response.
    Retrieves API key from Django settings: OPENROUTER_API_KEY
    """
    from django.conf import settings
    
    api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
    
    if not api_key:
        return "⚠️ Chatbot API key not configured. Please add OPENROUTER_API_KEY to Django settings."
    
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "DevBlog",
        }
        
        # Using a more reliable open-source model available on OpenRouter
        payload = {
            "model": "openai/gpt-3.5-turbo",  # Reliable model with free tier
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 200,
            "top_p": 0.95
        }
        
        print(f"[ChatBot] Sending request to OpenRouter API")
        print(f"[ChatBot] URL: {url}")
        print(f"[ChatBot] Model: {payload['model']}")
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        print(f"[ChatBot] Response Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"[ChatBot] Error Response: {response.text}")
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            error_msg = error_data.get('error', {}).get('message', 'API Error')
            return f"API Error: {error_msg}"
        
        response.raise_for_status()
        result = response.json()
        
        print(f"[ChatBot] Response received successfully")
        
        if 'choices' in result and len(result['choices']) > 0:
            reply = result['choices'][0]['message']['content'].strip()
            return reply
        else:
            print(f"[ChatBot] No choices in response: {result}")
            return "I couldn't generate a response. Please try again."
    
    except requests.exceptions.Timeout:
        print(f"[ChatBot] Timeout Error")
        return "Request timed out. Please try again."
    except requests.exceptions.ConnectionError as e:
        print(f"[ChatBot] Connection Error: {str(e)}")
        return "Connection error. Please check your internet and try again."
    except requests.exceptions.RequestException as e:
        print(f"[ChatBot] OpenRouter API Error: {str(e)}")
        return f"API Error: {str(e)[:100]}"
    except Exception as e:
        print(f"[ChatBot] Unexpected Error: {str(e)}")
        return f"Error: {str(e)[:100]}"
