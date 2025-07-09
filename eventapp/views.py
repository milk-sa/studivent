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
from django.views.decorators.http import require_POST, require_http_methods


# Create your views here.
@login_required
def home_view(request):
    return render(request, 'eventapp/events.html')
@login_required
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
@login_required
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



@login_required
def rsvp_status_view(request, event_id):
    try:
        has_joined = RSVP.objects.filter(user=request.user, event_id=event_id, status='yes').exists()
        return JsonResponse({'joined': has_joined})
    except event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

@login_required
def rsvp_count_view(request, event_id):
    count = RSVP.objects.filter(event_id=event_id, status='yes').count()
    return JsonResponse({'count': count})
@login_required
def event_detail_page(request, event_id):
    return render(request, 'eventapp/event_detail.html')

@login_required
def account_page(request):
    return render(request, 'eventapp/home.html')
@login_required
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
@login_required
def myevents(request):
    return render(request,"eventapp/my_events.html")
@login_required


def my_rsvped_events(request):
    if request.user.is_authenticated:
        # ✅ Filter for only 'yes' RSVPs by the logged-in user
        rsvps = RSVP.objects.filter(user=request.user, status='yes').select_related('event')

        events = []
        for rsvp in rsvps:
            event = rsvp.event
            print(f"RSVP event: {event.title}, RSVP user: {rsvp.user.username}, status: {rsvp.status}")

            events.append({
                'id': event.id,
                'title': event.title,
                'date': event.date.strftime('%Y-%m-%d'),
                'location': event.location,
            })

        return JsonResponse(events, safe=False)
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)



@csrf_exempt
@require_http_methods(["GET", "POST"])
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
    else:
        # GET request: show login form
        return render(request, 'eventapp/home.html')
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')




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
