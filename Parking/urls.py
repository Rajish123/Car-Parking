from django.urls import path

from .views import *

from knox import views as knox_views
# from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'parking'

urlpatterns = [
    # path('apilogin',MyObtainTokenPairView.as_view(),name = 'token_obtain_pair'),
    # path('apilogin/refresh', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('login',LoginAPI.as_view(), name = 'login'),
    path('logout', knox_views.LogoutView.as_view(), name = 'logout'),
    path('logout/all', knox_views.LogoutAllView.as_view, name = 'all-logout'),
    path('register',RegisterView.as_view(), name = 'register'),
    # path('register2',UserRegistration.as_view(), name = 'user-register'),
    path('view_profile',ViewProfile.as_view(), name = 'view-profile'),
    path('update_profile', UpdateProfile.as_view(), name = 'update-profile'),
    path('update_user/<str:id>', UpdateUser.as_view(), name = 'update-user'),
    path('parking',ParkingView.as_view(), name = 'parking'),
    # path('parking_space_check', ParkingSpaceCheck.as_view(), name = 'space-check'),
    path("car_entry/<str:pk>", CarEntry.as_view(),name = 'car-entry'),
    path('provide_ticket', ProvideTicket.as_view(),name = 'provide-ticket'),
    path('update_slot/<str:pk>',UpdateParkingSlotStatus.as_view(),name = 'update-slot'),
    path('car_exit/<str:pk>',ExitParking.as_view(),name = 'exit-parking'),
    path('update_ticket/<str:pk>',UpdateTicket.as_view(), name = 'update-ticket'),
    path('update_carstatus/<str:pk>', UpdateCarStatus.as_view(),name = 'update-carstatus'),
    path('bill/<str:pk>',BillGenerator.as_view(),name = 'bill'),
    path('payment/<str:pk>',Pay.as_view(),name = 'payment'),
    path('ticket_history',TicketHistory.as_view(),name = 'ticket-history'),
    path('payment_history',PaymentHistory.as_view(),name = 'payment-history')
]
