from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from revendedor.models import RevendedorUser
from revendedor.serializer import RegisterSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}


class CreateRevendedor(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            content = {'message': "Revendedor salvo com sucesso."}
            return JsonResponse(content, safe=False)


class ValidaLoginRevendedor(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = request.data

        # Parametros obrigatórios
        if not data.get('login'):
            content = {'message': "Login é obrigatório."}
            return JsonResponse(content, safe=False, status=400)
        if not data.get('senha'):
            content = {'message': "Senha é obrigatório."}
            return JsonResponse(content, safe=False, status=400)

        # Valida usuário
        user = authenticate(cpf=data.get('login'), password=data.get('senha'))
        if user is not None:
            content = {'message': "Usuário e senha válidos.", "valid": True}
            return JsonResponse(content, safe=False)
        content = {'message': "Login inválido.", "valid": False}
        return JsonResponse(content, safe=False)
