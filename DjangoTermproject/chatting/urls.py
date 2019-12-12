from .import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView




app_name = 'chatting'
urlpatterns = [
    path('select/',TemplateView.as_view(template_name='chatting/selectchat.html'),name='selectchat'),
    path('index/<int:select>/',views.indexView.as_view(),name='index'),
    path('room/<int:select>/<int:member>/',views.chatView.as_view(),name='chat'),
]