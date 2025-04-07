from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('message/', views.message_view, name='message'),
    path('prompt/', views.prompt_view, name='prompt'),
    path('reply/', views.twilio_automated_response, name='auto_response'),

    path('api/messages/', views.retrieve_messages_view, name='retrieve_messages'),

    path('api/model/', views.model_view, name='model'),
]