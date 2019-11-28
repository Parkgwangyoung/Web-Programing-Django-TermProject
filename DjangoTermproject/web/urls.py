from django.urls import path
from django.views.generic import TemplateView
from.import views

app_name ='web'
urlpatterns = [
   path('',views.indexView.as_view(),name='website'),
   path('assign/',views.assignView.as_view(),name='assign'),
   path('board/<int:board>/',views.BoardView.as_view(),name='board'),
   path('board/<int:board>/create/',views.CreateView.as_view(),name='createpost'),
   path('board/<int:board>/post/',views.postView.as_view(),name='post'),
   path('btcreate/',views.BtCreateView.as_view(),name='Btcreate'),
   path('btaccess/',views.BtAccessView.as_view(),name='Bcreate'),
]
