from django.urls import path
from . import views

urlpatterns = [
    path('note/', views.NoteAPI.as_view()),
]
