from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.middleware.csrf import get_token
from datetime import datetime, timedelta
import json
import jwt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

SECRET_KEY = 'mi_api_key_for_tokens_is_secret_**'

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        if not username or not password or not email:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        user = User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({'message': 'User created successfully', 'user_id': user.id}, status=201)

@csrf_exempt
def edit_user(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        username = data.get('username')
        email = data.get('email')
        try:
            user = User.objects.get(id=user_id)
            if username:
                user.username = username
            if email:
                user.email = email
            user.save()
            return JsonResponse({'message': 'User updated successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Autenticar usuario
        user = authenticate(username=username, password=password)
        if user is not None:
            # Generar tokens de acceso y refresh
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=HTTP_200_OK)

        return Response({'error': 'Credenciales inválidas'}, status=HTTP_401_UNAUTHORIZED)

@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = get_random_string(8)
            # user.set_password(new_password)
            # user.save()
            send_mail(
                'Password Reset',
                f'Your new password is: {new_password}',
                'admin@example.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Password reset successfully. Check your email.'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Email not found'}, status=404)

@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})

@csrf_exempt
def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})