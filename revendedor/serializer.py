import numbers

from rest_framework import serializers
from revendedor.models import RevendedorUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import re


class RegisterSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=RevendedorUser.objects.all())]
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=RevendedorUser.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = RevendedorUser
        fields = ('password', 'email', 'first_name', 'last_name', 'cpf', 'nome_completo')
        extra_kwargs = {
            'cpf': {'required': True},
            'nome_completo': {'required': True}
        }

    def create(self, validated_data):

        # cria nome e sobrenome pelo nome completo
        name = validated_data['nome_completo']
        last_name = ''
        parts = name.split(' ', 1)
        if len(parts) > 1:
            name, last_name = name.split(None, 1)

        user = RevendedorUser.objects.create(
            first_name=name,
            last_name=last_name,
            email=validated_data['email'],
            username=validated_data['cpf'],
            cpf=validated_data['cpf'],
            nome_completo=validated_data['nome_completo'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def validate_cpf(self, cpf):
        """ If cpf in the Brazilian format is valid, it returns True, otherwise, it returns False. """

        # Check if type is str
        if not isinstance(cpf, str):
            raise serializers.ValidationError('CPF inválido.')

        # Remove some unwanted characters
        cpf = re.sub("[^0-9]", '', cpf)

        # Verify if CPF number is equal
        if cpf == '00000000000' or cpf == '11111111111' or cpf == '22222222222' or cpf == '33333333333' or \
                cpf == '44444444444' or cpf == '55555555555' or cpf == '66666666666' or cpf == '77777777777' \
                or cpf == '88888888888' or cpf == '99999999999':
            raise serializers.ValidationError('CPF inválido.')

        # Checks if string has 11 characters
        if len(cpf) != 11:
            raise serializers.ValidationError('CPF inválido.')

        sum = 0
        weight = 10

        """ Calculating the first cpf check digit. """
        for n in range(9):
            sum = sum + int(cpf[n]) * weight

            # Decrement weight
            weight = weight - 1

        verifying_digit = 11 - sum % 11

        if verifying_digit > 9:
            first_verifying_digit = 0
        else:
            first_verifying_digit = verifying_digit

        """ Calculating the second check digit of cpf. """
        sum = 0
        weight = 11
        for n in range(10):
            sum = sum + int(cpf[n]) * weight

            # Decrement weight
            weight = weight - 1

        verifying_digit = 11 - sum % 11

        if verifying_digit > 9:
            second_verifying_digit = 0
        else:
            second_verifying_digit = verifying_digit

        if cpf[-2:] == "%s%s" % (first_verifying_digit, second_verifying_digit):
            return cpf
        raise serializers.ValidationError('CPF inválido.')
