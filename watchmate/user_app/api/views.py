from rest_framework.response import Response
from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status

# JWT toen authentication
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Registered Successfully!"
            data['username'] = account.username
            data['email'] = account.email
            
            # JWT Token Authentication
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
            # Token Authentication
            # token, created = Token.objects.get_or_create(user=account)
            # data['token'] = token.key



        else:
            data = serializer.errors

        return Response(data)
