from django.urls import path
from . import views
from .views import rsvp_view


urlpatterns = [
    path('home/', views.home_view, name='home'), 
    path('events/', views.list_events, name='home'),
    path('events/<int:pk>/', views.event_detail, name='event-detail'),
    path('events/<int:event_id>/view/', views.event_detail_page, name='event-detail-page'),
    path('reg/',views.register_page),
    path('register/', views.register_view, name='register'),
    path('', views.account_page, name='account'),
    path('event/<int:event_id>/rsvp-count/', views.rsvp_count_view, name='rsvp_count'),


    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('event/<int:event_id>/rsvp/', rsvp_view, name='rsvp'),
    path('event/<int:event_id>/rsvp-status/', views.rsvp_status_view, name='rsvp_status'),
    path('my_rsvped_events/', views.my_rsvped_events, name='my_rsvped_events'),

    path('myevents/',views.myevents, name = 'myevents')
    



]

