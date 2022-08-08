from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from revendedor.models import RevendedorUser
from revendedor.serializer import RegisterSerializer, GroupSerializer, CompraViewSerializer
from revendedor.models import Compra
import requests
import os
import re
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class ValidaLoginRevendedor(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = request.data

        # Parametros obrigatórios
        if not data.get('login'):
            logger.warning('Login é obrigatório na validação de login revendedor')
            content = {'statusCode': 400, 'body': {'message': "Login é obrigatório"}}
            return JsonResponse(content, safe=False, status=400)
        if not data.get('senha'):
            logger.warning('Senha é obrigatório na validação de login revendedor')
            content = {'statusCode': 400, 'body': {'message': "Senha é obrigatório"}}
            return JsonResponse(content, safe=False, status=400)

        # Valida usuário
        user = authenticate(cpf=data.get('login'), password=data.get('senha'))
        if user is not None:
            content = {'statusCode': 200, 'body': {'message': "Login válido", "valid": True}}
            return JsonResponse(content, safe=False)
        content = {'statusCode': 200, 'body': {'message': "Login inválido", "valid": False}}
        return JsonResponse(content, safe=False)


class CompraViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows purchases to be viewed or edited.
    """
    queryset = Compra.objects.all().order_by('-data')
    serializer_class = CompraViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    purchase_tier1 = int(os.getenv("PURCHASE_TIER_1"))
    tier1_percent = int(os.getenv("PURCHASE_TIER_1_PERCENTAGE"))
    purchase_tier2 = int(os.getenv("PURCHASE_TIER_2"))
    tier2_percent = int(os.getenv("PURCHASE_TIER_2_PERCENTAGE"))
    purchase_tier3 = int(os.getenv("PURCHASE_TIER_3"))
    tier3_percent = int(os.getenv("PURCHASE_TIER_3_PERCENTAGE"))

    def create(self, request, *args, **kwargs):
        if "valor" in request.data:
            valor = float(request.data['valor'])
            data = self.define_cashback(valor, request.data)
        if "revendedor" in request.data:
            request.data['revendedor'] = re.sub("[^0-9]", "", request.data['revendedor'])

        serializer = CompraViewSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def define_cashback(self, value, data):
        if value < self.purchase_tier1:
            data['porcentagem'] = self.tier1_percent
            cashback = float(value) / 100 * float(self.tier1_percent)
            data['valor_cashback'] = "{:.2f}".format(cashback)
        if self.purchase_tier2 < value > self.purchase_tier1:
            data['porcentagem'] = self.tier2_percent
            cashback = float(value) / 100 * float(self.tier2_percent)
            data['valor_cashback'] = "{:.2f}".format(cashback)
        if value > self.purchase_tier3:
            data['porcentagem'] = self.tier3_percent
            cashback = float(value) / 100 * float(self.tier3_percent)
            data['valor_cashback'] = "{:.2f}".format(cashback)

        return data


class RevendedoresViewSet(viewsets.ModelViewSet):
    """
    View to list all resellers in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    queryset = RevendedorUser.objects.all().order_by('-date_joined')
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if "cpf" in request.data:
            request.data['cpf'] = re.sub("[^0-9]", "", request.data['cpf'])
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class AcumuladoCashback(APIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data

        # Parametros obrigatórios
        if not data.get('cpf'):
            content = {'statusCode': 400, 'body': {'message': "CPF é obrigatório"}}
            return JsonResponse(content, safe=False, status=400)

        url = os.getenv('BOTICARIO_API_URL').format(data.get('cpf'))
        header = {
            "Content-Type": "application/json",
            "token": os.getenv('BOTICARIO_API_TOKEN')
        }

        try:
            result = requests.get(url, headers=header)
            if result.status_code == 200:
                content = result.json()
                return JsonResponse(content, safe=False)
        except requests.exceptions.MissingSchema as e:
            logger.error(f"URL: {url}. Houve um erro na URL da API: {e}")
            content = {'statusCode': 500, 'body': {'message': f"Houve um erro na URL da API: {e}"}}
            return JsonResponse(content, safe=False, status=500)
        except requests.exceptions.RequestException as err:
            logger.error(f"URL: {url}. Houve um erro na requisição: {err}")
            content = {'statusCode': 400, 'body': {'message': f"Houve um erro na requisição: {err}"}}
            return JsonResponse(content, safe=False, status=400)
        except requests.exceptions.HTTPError as errh:
            logger.error(f"URL: {url}. Houve um erro http: {errh}")
            content = {'statusCode': 400, 'body': {'message': f"Houve um erro http: {errh}"}}
            return JsonResponse(content, safe=False, status=400)
        except requests.exceptions.ConnectionError as errc:
            logger.error(f"URL: {url}. Houve um erro de conexão: {errc}")
            content = {'statusCode': 400, 'body': {'message': f"Houve um erro de conexão: {errc}"}}
            return JsonResponse(content, safe=False, status=400)
        except requests.exceptions.Timeout as errt:
            logger.error(f"URL: {url}. Timeout: {errt}")
            content = {'statusCode': 400, 'body': {'message': f"Timeout: {errt}"}}
            return JsonResponse(content, safe=False, status=400)

        logger.error(f"URL: {url}. Houve um erro não identificado.")
        content = {'statusCode': 400, 'body': {'message': "Houve um erro não identificado."}}
        return JsonResponse(content, safe=False, status=400)
