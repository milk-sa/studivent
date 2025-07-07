from django.urls import path
from . import views
from .views import rsvp_view


urlpatterns = [
    path('', views.home_view, name='home'), 
    path('events/', views.list_events, name='home'),
    path('events/<int:pk>/', views.event_detail, name='event-detail'),
    path('events/<int:event_id>/view/', views.event_detail_page, name='event-detail-page'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('event/<int:event_id>/rsvp/', rsvp_view, name='rsvp'),
    

]

