from rest_framework import views, permissions, status
from rest_framework.response import Response
from knox.auth import AuthToken, hash_token

from . import serializers as user_serializer
from . import services
from . import authentication


class RegisterApi(views.APIView):

    def post(self, request):
        serializer = user_serializer.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        serializer.instance = services.create_user(user_dc=data)

        return Response(data=serializer.data)


class LoginApi(views.APIView):
    def post(self, request):
        serializer = user_serializer.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # email = request.data["email"]
        # password = request.data["password"]

        # user = services.user_email_selector(email=email)

        # if user is None:
        #     raise exceptions.AuthenticationFailed("Invalid credentials")

        # if not user.check_password(raw_password=password):
        #     raise exceptions.AuthenticationFailed("Invalid credentials")

        # token = services.create_token(user_id=user.id)

        user = serializer.validated_data['user']

        _, token = AuthToken.objects.create(user=user)

        serializer = user_serializer.UserSerializer(user)

        response = Response(data={"user": serializer.data, "token": token})

        return response


class UserApi(views.APIView):

    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = user_serializer.UserSerializer(user)

        return Response(serializer.data)

    def post(self, request):

        keys = request.data.keys()

        required_keys = ['first_name', 'last_name']

        is_valid = all(elem in keys for elem in required_keys)

        if not is_valid:
            return Response(data={"message": "Please provide updated user data"}, status=status.HTTP_412_PRECONDITION_FAILED)

        user = request.user

        serializer = user_serializer.UserSerializer()

        serializer.instance = services.update_user(
            user=user, data=request.data)

        return Response(data=serializer.data)


class UsersApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        users = services.get_all_users()

        serializer = user_serializer.UserSerializer(users, many=True)

        return Response(serializer.data)


class LogoutApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        response = Response()

        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            t = token.split(" ")
            token = t[2]

        if not token:
            return None

        hashed = hash_token(token=token)

        AuthToken.objects.filter(digest=hashed).delete()
        response.data = {"message": "Logged out successfully"}

        return response


class LogoutAllApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        response = Response()
        user = request.user

        AuthToken.objects.filter(user=user).delete()
        response.data = {"message": "Logged out successfully"}

        return response
