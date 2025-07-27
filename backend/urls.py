
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, LoginView,
    AddEventView, ListEventView,
    EditEventView, DeleteEventView, UserDetailView,
    register_for_event, CancelRegistrationView,
    LogoutView, DeleteAccountView, MyEventsView, registered_events, EditEventView, EventParticipantsView
)

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserDetailView.as_view(), name='user-detail'),

    # Events (Coordinator)
    path('events/add/', AddEventView.as_view(), name='add-event'),
    path('events/', ListEventView.as_view(), name='list-events'),
    path('events/edit/<int:pk>/', EditEventView.as_view(), name='edit-event'),
    path('events/delete/<int:pk>/', DeleteEventView.as_view(), name='delete-event'),
    path('participants/<int:event_id>/', EventParticipantsView.as_view(), name='event-participants'),  # Removed 'api/' prefix

    # Events (Participant)
    path('events/<int:event_id>/register/', register_for_event, name='register-event'),
    path('events/<int:event_id>/cancel/', CancelRegistrationView.as_view(), name='cancel-registration'),
    path('events/registered/', registered_events, name='registered-events'),

    # Account Management
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),

    # Event History View (Participant)
    path('events/my-events/', MyEventsView.as_view(), name='my-events'),
]
