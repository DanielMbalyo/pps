import uuid

from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from .serializers import UserSerializer, LoginSerializer
from .utils import generate_access_token, generate_refresh_token

User = get_user_model()

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        response = Response()
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            response.status_code = HTTP_400_BAD_REQUEST
            response.data = {'success': "False", 'message': "Both Email and Password are required.",}
            return response
        user = User.objects.filter(email=email)
        if user is not None:
            not_active = user.filter(is_active=False)
            if not_active.exists():
                link = reverse('account:resend_activation')
                reconfirm_msg = """Go to <a href='{resend_link}'>
                resend confirmation email</a>.
                """.format(resend_link=link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                response.data = {'success': "False", 'message': "Activation Mail Has Sent To Your Inbox.",}
                return response
                if is_confirmable:
                    response.data = {'success': "False", 'message': "Please check your email to confirm your account.",}
                    return response
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    response.data = {'success': "False", 'message': "Email not confirmed.",}
                    return response
                if not is_confirmable and not email_confirm_exists:
                    response.status_code = HTTP_401_UNAUTHORIZED
                    response.data = {'success': "False", 'message': "This user is inactive.",}
                    return response
            if not user.first().check_password(password):
                response.data = {'success': "False", 'message': "Wrong Password.",}
                return response
            serialized_user = UserSerializer(user.first()).data
            access_token = generate_access_token(user.first())
            refresh_token = generate_refresh_token(user.first())
            response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
            response.data = {
                'success': "True", 'message': "Successfully Authenticated.", 
                'access_token': access_token, 'user': serialized_user,
            }
            return response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            response.data = {'success': "False", 'message': "User Not Found.",}
            return response

class RefreshAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refreshtoken')
        if refresh_token is None:
            response.status_code = HTTP_401_UNAUTHORIZED
            response.data = {'success': "False", 'message': 'Authentication credentials were not provided.',}
            return response
        try:
            payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Expired refresh token, Please login again.')

        user = User.objects.filter(uid=uuid.UUID(payload.get('user_id'))).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            response.status_code = HTTP_401_UNAUTHORIZED
            response.data = {'success': "False", 'message': "This user is inactive.",}
            return response

        access_token = generate_access_token(user)
        return Response({'access_token': access_token})