
from django.urls import path
from .import views
from django.views.generic import TemplateView


app_name ='login'
urlpatterns = [
   path('',views.loginView.as_view(),name='login'),
   path('access/',TemplateView.as_view(template_name='login/access.html'),name='access'),
   path('signin/<int:pk>/',views.signinView.as_view(),name='signin'),
   path('logout/',views.LogoutView.as_view(),name='logout'),
   path('update/',views.updateView.as_view(),name='update'),
]
