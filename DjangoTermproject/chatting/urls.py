from .import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static




app_name = 'chatting'
urlpatterns = [
    path('',views.chatView.as_view(),name='chat'),
]