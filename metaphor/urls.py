from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate_all, name='generate_all'),
    path('history/', views.history, name='history'),  # 履歴表示ページのURL
    path('delete/<int:pk>/', views.delete_history, name='delete_history'),  # ← 削除用
]
