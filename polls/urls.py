from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('polls/<int:pk>/', views.DetailView.as_view(), name='details'),
    path('polls/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('polls/new/', views.new_poll, name='new_poll'),
    path('polls/<int:pk>/vote/', views.vote, name='vote'),
    path('polls/<int:pk>/delete/', views.delete_poll, name='delete_poll'),

]
