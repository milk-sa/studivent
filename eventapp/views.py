from django.shortcuts import get_object_or_404, redirect,render
from .models import event,RSVP
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

# Create your views here.
def home_view(request):
    return render(request, 'eventapp/events.html')

def list_events(request):
    events = event.objects.all().order_by('-date')
    data = [
        {
            "id": event.id,
            "title": event.title,
            "date": event.date.strftime("%Y-%m-%d")
        }
        for event in events
    ]
    return JsonResponse(data, safe=False)

def event_detail(request, pk):
    e = get_object_or_404(event, pk=pk)  # ← fetch single event object
    data = {
        "id": e.id,
        "title": e.title,
        "date": e.date.strftime("%Y-%m-%d"),
        "location": e.location,
        "description": e.description,
    }
    return JsonResponse(data)


def event_detail_page(request, event_id):
    return render(request, 'eventapp/event_detail.html')

def account_page(request):
    return render(request, 'eventapp/home.html')

def register_page(request):
    return render(request,'eventapp/register.html')


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        form = RegisterForm(data)

        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # starts session
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        response = JsonResponse({'message': 'Logout successful'})
        print("Logout response:", response.content)  # Debug
        return response
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .models import event, RSVP

@csrf_exempt
@login_required
def rsvp_view(request, event_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')

            if status not in ['yes', 'no']:
                return JsonResponse({'error': 'Status must be "yes" or "no".'}, status=400)

            event_obj = event.objects.get(id=event_id)
            user = request.user

            rsvp, created = RSVP.objects.update_or_create(
                user=user,
                event=event_obj,
                defaults={'status': status}
            )

            return JsonResponse({
                'message': f'RSVP {"created" if created else "updated"} successfully',
                'status': rsvp.status
            })

        except event.DoesNotExist:
            return JsonResponse({'error': 'Event not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    return JsonResponse({'error': 'Only POST allowed.'}, status=405)
