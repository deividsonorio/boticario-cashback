import unittest
from django.test import TestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from revendedor.models import RevendedorUser, Compra
from django.db.utils import IntegrityError
from rest_framework.test import APIRequestFactory, APIClient
import requests
from django.urls import reverse
from django.test import Client

class CashbackTestCase(TestCase):

    cpf_test = '08360313938'
    email_test = 'teste@teste.com'
    password = '123-asd-398'

    def setUp(self):
        RevendedorUser.objects.filter(username=self.cpf_test).delete()
        revendedor = RevendedorUser.objects.create(username=self.cpf_test, email=self.email_test, cpf=self.cpf_test, password=self.password)
        compra = Compra.objects.create(
            revendedor=revendedor,
            codigo='123',
            data='2022-01-01',
            valor=100,
            porcentagem=10,
            status='V',
            valor_cashback=10,
        )

    def test_login_unauthorized(self):
        """Unauthorized login test"""
        c = Client()
        response = c.post(reverse('token_obtain_pair'), {'cpf': self.cpf_test, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, f'O status retornado deveria ser 401')

    def test_login_jwt(self):
        """Login with jwt test"""
        user = RevendedorUser.objects.create_user(
            username='john', cpf='12819447007', email='js@js.com', password='jwt.tes')
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        self.assertIsInstance(refresh, RefreshToken)

        login_data = {
            'cpf': '12819447007',
            'password': 'jwt.tes'
        }

        url = reverse('token_obtain_pair')
        response = client.post(url, login_data, format='json')

        # test token
        self.assertTrue(response.data['access'])

        # test refresh
        self.assertTrue(response.data['refresh'])

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # test access to revendedor list/creation
        response = client.get('/api/revendedor/', data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test access to compra list/creation
        response2 = client.get('/api/compra/', data={'format': 'json'})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_revendedor_duplicated_cpf_fail(self):
        """Revendedor creation with already used cpf"""
        with self.assertRaises(IntegrityError, msg='O cpf deve ser único'):
            RevendedorUser.objects.create(username=self.cpf_test)

    def test_revendedor_undefined(self):
        """Revendedor not created query test"""
        with self.assertRaises(RevendedorUser.DoesNotExist, msg='Revendedor inexistente'):
            RevendedorUser.objects.get(username="123")

    def test_revendedor_created(self):
        """Revendedor already created tes"""
        test = RevendedorUser.objects.get(username=self.cpf_test)
        self.assertEqual(RevendedorUser.objects.count(), 1)
        self.assertEqual(test.username, self.cpf_test, f'O username deveria ser: "{self.cpf_test}"')
        self.assertEqual(test.email, "teste@teste.com", f'O email deveria ser "{self.email_test}"')
        self.assertTrue(self.cpf_test in str(test))

    def test_compra_creation_fail(self):
        """Compra creation fail test"""
        with self.assertRaises(TypeError, msg='Compra com parâmetro inválido'):
            Compra.objects.create(teste="123")

    def test_compra_creation(self):
        """Compra creation test"""
        revendedor = RevendedorUser.objects.get(username=self.cpf_test)
        compra = Compra.objects.create(
            revendedor=revendedor,
            codigo=123,
            data='2022-01-01',
            valor=100,
            porcentagem=10,
            status='V',
            valor_cashback=10,
        )

        self.assertEqual(compra.revendedor_id, self.cpf_test, f'O revendedor da compra deveria ser: "{self.cpf_test}"')
        self.assertEqual(compra.codigo, 123, f'O código da compra deveria ser 123')
        self.assertEqual(compra.valor, 100, f'O valor da compra deveria ser 100')
        self.assertEqual(compra.porcentagem, 10, f'A porcentagem da compra deveria ser 10')
        self.assertEqual(compra.status, 'V', f'O status da compra deveria ser "V"')
        self.assertEqual(compra.valor_cashback, 10, f'O cashback da compra deveria ser 10')

    def test_cashback(self):
        user = RevendedorUser.objects.create_user(username='cashback',
                                                  cpf='12819447007', email='js@js.com', password='jwt.tes')
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        self.assertIsInstance(refresh, RefreshToken)

        login_data = {
            'cpf': '12819447007',
            'password': 'jwt.tes'
        }

        url = reverse('token_obtain_pair')
        response = client.post(url, login_data, format='json')

        # test token
        self.assertTrue(response.data['access'])

        # test refresh
        self.assertTrue(response.data['refresh'])

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # cashback sem cpf
        response = client.post('/api/revendedor/cashback/', data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # cashback com cpf
        response = client.post('/api/revendedor/cashback/', data={'cpf': '12819447007', 'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
