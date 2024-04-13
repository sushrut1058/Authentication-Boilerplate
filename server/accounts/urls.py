from django.urls import path, include
from .views import signup, login, verify_email, validate_token, resend_email, TokenVerificationView, onboard

urlpatterns = [
    path('signup', signup, name='signup'),
    path('login',login, name='login'),
    path('validate_token/', TokenVerificationView.as_view(), name='validate_token'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('verify-email/<int:user_id>/<str:token>/', verify_email, name='verify_email'),
    path ('resend_email', resend_email, name='resend_email'),
    path ('onboard', onboard, name='onboard')
]
