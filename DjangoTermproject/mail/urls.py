from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from.import views


app_name='mail'
urlpatterns = [
    path('',views.MailIndexView.as_view(),name='mailindex'),
    path('<int:mail_id>/',views.MailDetailView.as_view(),name='mail'),
    path('create/',views.CreateMailView.as_view(),name='createmail'),
]