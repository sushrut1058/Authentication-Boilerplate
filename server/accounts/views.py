from .serializers import UserSerializer
from rest_framework import status
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.views import APIView

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        verification_token = user.generate_verification_token()
        
        verification_url = request.build_absolute_uri(reverse('verify_email', args=[user.id, verification_token]))
        
        send_verification_email(user.email, verification_url)

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    print(email, password)
    user = authenticate(username=email, password=password)
    print(user)
    if user:
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        data = {
            'user':serializer.data,
            'access':str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def validate_token(request):
    try:
        token = request.data.get('token')
        valid_data = AccessToken(token)  # Verifies the token
        user_id = valid_data['user_id']
        print(user_id, token)
        user = CustomUser.objects.get(id=user_id)
        user_data = {
            "id": user.id,
            "email": user.email,
            # Add any additional fields you need
        }
        return Response({
            'user': user_data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
class TokenVerificationView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        user = UserSerializer(request.user)
        return Response({
                'user':user.data,
            }, status=status.HTTP_200_OK)
            

@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def onboard(request):
    try:
        role = request.data.get('role')
        user = request.user
        if role=="Hunt":
            user.role = 1
        elif role=="Hire":
            user.role=2
        user.is_onboarded=True
        user.save()
        return Response({"message": "Onboarded Successfully"},status=status.HTTP_200_OK)
    except:
        return Response({"error":"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def verify_email(request, user_id, token):
    try:
        user = CustomUser.objects.get(id=user_id, email_verification_token=token)
        user.is_email_verified = True
        user.email_verification_token = ''
        user.save()
        return Response({"message": "Email verified successfully."})
    except:
        return Response({"error":"The link is either invalid or the user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])    
def resend_email(request):
    try:
        token = request.data.get('token')
        print(111)
        valid_data = AccessToken(token)
        user = CustomUser.objects.get(id=valid_data['user_id'], is_email_verified=False)
        if user:
            verification_url = request.build_absolute_uri(reverse('verify_email', args=[user.id, user.email_verification_token]))
            send_verification_email(user.email, verification_url)
            return Response({"message":"Email sent successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No user found!"}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"error": "User not found or already verified."}, status=status.HTTP_404_NOT_FOUND)
    except (TokenError, InvalidToken):
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        # Log the exception for debugging purposes
        print(e)  # Consider using logging instead of print in production
        return Response({"error": "Something went wrong!"}, status=status.HTTP_400_BAD_REQUEST)
    
def send_verification_email(user_email, verification_url): 
    send_mail(
        'Verify your email',
        f'Please click on the link to verify your email: {verification_url}',
        'sushrut1058@gmail.com',
        [user_email],
        fail_silently=False,
    )