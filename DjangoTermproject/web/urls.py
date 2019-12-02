from django.urls import path
from django.views.generic import TemplateView
from.import views

app_name ='web'
urlpatterns = [
  path('',views.indexView.as_view(),name='website'),
   path('assign/',views.assignView.as_view(),name='assign'),
   path('selboard/',TemplateView.as_view(template_name='web/selCreateBoard.html'), name='Selcreate'),
   path('board/<int:boardtable>/',views.BoardAccessView.as_view(),name='boardaccess'),
   path('board/<int:boardtable>/<int:board>/',views.BoardView.as_view(),name='board'),
   path('<int:boardtable>/<int:board>/create/',views.CreatepostView.as_view(),name='createpost'),
   path('board/<int:post>/post/',views.PostView.as_view(),name='post'),
   path('board/<int:post>/updatepost/',views.UpdatePostView.as_view(),name='updatepost'),
   path('board/<int:post>/deletepost/',views.DeletePostView.as_view(),name='deletepost'),
   path('btcreate/',views.BtcreateView.as_view(),name='Btcreate'),
   path('bcreate/',views.BcreateView.as_view(),name='Bcreate'),
   path('bpcreate/',views.BpCreateView.as_view(),name='Bpcreate'),
   path('board/<int:post>/like/',views.likeView.as_view(),name='like'),

]
