import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from core.forms import UserForm, UserProfileForm
from django.core.context_processors import csrf

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from serializers import UserSerializer


def main(request):
    data = {'user': request.user}
    data.update(csrf(request))
    print request.user
    return render_to_response('index.html', data)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    print request.data

    if serializer.is_valid():
        user = serializer.save()
        user.set_password(user.password)
        user.save()
        password = request.data.get('password')

        user = authenticate(username=user.username, password=password)
        login(request, user)

        return Response({"status": "good"})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    # data = json.loads(request.body)
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        if user.is_active:
            login(request, user)
            name = '%s %s' %(user.first_name, user.last_name)
            response = Response({'username': name}, status=status.HTTP_200_OK)
            response.set_cookie('user', user.id)
            response.set_cookie('username', name)
            return response
        else:
            return Response({'error': 'Your account is disabled.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid login details supplied.'}, status=status.HTTP_400_BAD_REQUEST)


def me(request):
    if request.user.is_authenticated():
        username = "%s %s" %(request.user.first_name, request.user.last_name)
    else:
        username = ''
    data = {"is_login": request.user.is_authenticated(),
            "username": username}
    return JsonResponse(data)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:landing_page'))

def user_profile(request):
    data = {"user": request.user}

    return render_to_response('user_page_profile.html', data)


def past_searches(request):
    # TODO: add searches
    return render_to_response('user_page_searches.html')