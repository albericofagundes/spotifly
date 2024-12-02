# users/views.py
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# View de Registro de Usuário
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Retorna os dados do novo usuário
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View de Login de Usuário
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Verifica se o usuário existe e as credenciais são válidas
    user = authenticate(request, username=email, password=password)
    if user is not None:
        # Gera o token JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    return Response({'error': 'Credenciais inválidas'}, status=400)
