from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate_all, name='generate_all'),
    path('history/', views.history, name='history'),  # 履歴表示ページのURL
]
