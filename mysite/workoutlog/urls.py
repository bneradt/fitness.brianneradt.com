from django.urls import path
from .views import (
    WorkoutSessionListView,
    WorkoutSessionDetailView,
    WorkoutSessionCreateView,
    WorkoutSessionUpdateView,
    WorkoutSessionDeleteView,
)

app_name = 'workoutlog'
urlpatterns = [
    # Create a new session - the default view.
    path('', WorkoutSessionCreateView.as_view(), name='new_workout_session'),
    path('new_session/', WorkoutSessionCreateView.as_view(), name='new_workout_session'),
    # List existing sessions
    path('view_sessions/', WorkoutSessionListView.as_view(), name='view_workout_sessions'),
    # Detail view for a specific session
    path('session/<int:pk>/', WorkoutSessionDetailView.as_view(), name='workout_session_detail'),
    # Edit a session
    path('edit_session/<int:pk>/', WorkoutSessionUpdateView.as_view(), name='edit_workout_session'),
    # Delete a session
    path('delete_session/<int:pk>/', WorkoutSessionDeleteView.as_view(), name='delete_workout_session'),
]
