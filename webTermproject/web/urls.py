from django.urls import path
from django.views.generic import TemplateView
from .import views

app_name = 'web'
urlpatterns = [
    path('',views.loginView.as_view(),name='login'),
    path('access/',TemplateView.as_view(template_name='web/access.html'),name='access'),
    path('signin/<int:pk>/',views.signinView.as_view(),name='signin'),
    path('login/',views.loginView.as_view(),name='loginaccess'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('update/',views.updateView.as_view(),name='update'),
    path('assign/',views.assignView.as_view(),name='assign'),
    path('board/<int:pk>/<int:tk>/',views.BoardView.as_view(),name='board'),
    path('board/<int:pk>/<int:tk>/<int:ak>/',views.BoardAccessView.as_view(),name='boardaccess'),
    path('board/<int:pk>/<int:tk>/create/',views.Create_PostView.as_view(),name='createpost'),
    path('website/',TemplateView.as_view(template_name='web/website.html'),name='website'),
    path('test/',TemplateView.as_view(template_name='web/test.html'),name='test'),
    path('board/<int:pk>/<int:tk>/require/',views.reqireView.as_view(),name='reqire'),
    
]
