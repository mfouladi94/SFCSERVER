import json

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user_accounts.models import UserProfile
from user_accounts.serializers import UserProfileSerializer
from utils import apiResponses
from utils.apiResponses import APIResponse
from .serializers import *
import logging

logger = logging.getLogger('serverLogger')


@api_view(['POST'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def signup(request):
    try:
        ref_code = request.GET.get('ref')
        referrer = None

        if ref_code:
            try:
                referrer = UserProfile.objects.get(referral_code=ref_code)
            except UserProfile.DoesNotExist:
                referrer = None

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                UserProfile.objects.create(user=user)

                login(request, user)
                return apiResponses.APIResponse(status=apiResponses.OK, code=apiResponses.CODE_SUCCESS,
                                                messages="Registered Successfully")

            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])

            return apiResponses.APIResponse(status=apiResponses.NOK, code=apiResponses.CODE_Failed,
                                            messages=error_string)

        return apiResponses.APIResponse(status=apiResponses.NOK, code=apiResponses.CODE_Failed,
                                        messages="Not allowed Method")
    except Exception as e:
        return apiResponses.APIResponse(status=apiResponses.NOK, code=apiResponses.CODE_Failed,
                                        messages="Error in registration")



@api_view(['POST'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def login_by_username_phone_email(request):
    try:
        serializer_input = LoginSerializerInput(data=request.data)

        if not serializer_input.is_valid():
            return APIResponse(status=apiResponses.NOK, code=apiResponses.CODE_Failed, messages="data is not valid")

        data = serializer_input.validated_data
        username = data.get('username')
        password = data.get('password')


        # find user using email
        user = User.objects.filter(email=username).first()

        if user is None:
            user = User.objects.filter(username=username).first()

        if user is None and username.isdigit():
            phone_number = int(username)
            profile = UserProfile.objects.filter(
                mobile_number=phone_number).first()
            if profile is not None:
                user = profile.user

        if user is None:
            logger.info("wrong username" + json.dumps(data))
            return APIResponse(status=apiResponses.NOK, code=apiResponses.CODE_Failed, messages="user not found !")

        # fetching profile of user
        user_profile = UserProfile.objects.filter(user=user).first()

        if user_profile is None:
            logger.info("user profile doesn't exist " + json.dumps(data))
            return APIResponse(status=apiResponses.NOK, code=apiResponses.CODE_Failed,
                               messages="user profile doesn't exist ! contact administrator")

        if not user.check_password(password):
            logger.info("wrong password" + json.dumps(data))

            return APIResponse(status=apiResponses.NOK, code=apiResponses.CODE_Failed,
                               messages="credential is not valid !")

        JWTTPKENREFRESH = RefreshToken.for_user(user)


        response = {
            "id": user.id,
            "email": user.email,
            'refresh': str(JWTTPKENREFRESH),
            'access': str(JWTTPKENREFRESH.access_token),
            "userName": user.username,
            "phoneNumber": user_profile.mobile_number
        }

        return APIResponse(status=apiResponses.OK, code=apiResponses.CODE_SUCCESS, messages="Login successfully",
                           data=response)
    except Exception as e:
        logger.error("Error in Login Process!" + str(e.args))
        return APIResponse(status=apiResponses.NOK, code=apiResponses.CODE_Failed, messages="Error in Login Process!")


class ProfileApi(APIView):

    def get(self, request):
        try:

            if request.method == 'GET':
                userprofile = UserProfile.objects.get(user=request.user)
                serializer = UserProfileSerializer(userprofile)

                return apiResponses.APIResponse(status=apiResponses.OK, code=apiResponses.CODE_SUCCESS,
                                                messages="success", data=serializer.data)

            return apiResponses.APIResponse(status=apiResponses.NOK, code=apiResponses.CODE_Failed,
                                            messages="Not allowed Method")
        except Exception as e:
            print(e)
            return apiResponses.APIResponse(status=apiResponses.NOK, code=apiResponses.CODE_Failed,
                                            messages="Error in fetching profile")
