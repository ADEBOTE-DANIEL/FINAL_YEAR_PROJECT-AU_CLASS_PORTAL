
from django.urls import path
from . import views

urlpatterns = [
    # URL for the assignment marking page
    path('mark-assignment/', views.mark_assignment, name='mark_assignment'),
]
