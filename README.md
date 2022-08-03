<p>
<img src="https://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN"/>
<img src="https://img.shields.io/static/v1?label=licene&message=MIT&color=green" />
</p>

# Desafio Boticário

*O Boticário tem várias soluções para ajudar seus revendedores(as) a gerir suas finanças e
alavancar suas vendas. Também existem iniciativas para impulsionar as operações de vendas
como metas gameficadas e desconto em grandes quantidades de compras.*

*Agora queremos criar mais uma solução, e é aí que você entra com seu talento ;)*

*A oportunidade proposta é criar um sistema de Cashback, onde o valor será disponibilizado
como crédito para a próxima compra da revendedora no Boticário;*

*Cashback quer dizer “dinheiro de volta”, e funciona de forma simples: o revendedor faz uma
compra e seu benefício vem com a devolução de parte do dinheiro gasto no mês seguinte.*

*Sendo assim o Boticário quer disponibilizar um sistema para seus revendedores(as)
cadastrarem suas compras e acompanhar o retorno de cashback de cada um.*

## Requisitos técnicos obrigatórios
- Nodejs ou Python
- Docker
- Banco de dados relacional ou não relacional

## Funcionalidades e diferenciais

- [x] Login JWT
- [x] Validação de login
- [x] Refresh token
- [x] Cadastro de Revendedores
- [x] Cadastro de Compra
- [x] Consulta cashback (API externa como solicitado)
- [x] Testes
- [x] Migrations
- [x] Logs
- [x] Docker facilitando subir os ambientes 

## Tecnologias utilizadas

- Python 3.10
- Django 4.0.6
- REST
- JWT
- PostgreSQL
- Docker
- Git

# Dependências

* Docker - [Instalando o Docker](https://docs.docker.com/desktop/)
* Docker compose - [Instalando o Docker Compose](https://docs.docker.com/compose/install/)
* GIT [Instalando o Git](https://git-scm.com/book/pt-br/v2/Come%C3%A7ando-Instalando-o-Git)
<br>
<br>
<hr>

# Iniciando e utilizando o projeto

1. Clonando o repositório

```bash
git clone git@github.com:deividsonorio/boticario-cashback.git
```

2. Na pasta clonada do projeto, acesse a pasta **docker** e rode o comando:

```bash
docker-compose up -d
```
3. Serão criados os contâiners necesários para aplicação.

- sistema: Contâiner do aplicativo
- postgresql: Banco de dados PostgreSQL


4. A aplicação estará disponível em:

* <http://localhost:8000/>

<br>

**OBS**: será necessário um token de autenticação (JWT) para o acesso aos endpoints.

Para fins de teste, um super usuário é criado automaticamente ao iniciar a aplicação:

**cpf**: 08360313938<br>
**password**: teste123

É possível criar mais usuários (revendedores) através do endpoint de criação de revendedor (necessário autenticação).


<br>
<hr>

# API REST

Aqui estão exemplos de chamadas cURL para os endpoints. Você também pode utilizar outros métodos para consumir os endpoints como o HTTPie ou Postman.

![Imagem da tela de_login_django](./readme_images/login_curl.png?raw=true "Imagem da tela inicial da API")

Ou, alternativamente, use a interface da web do Django acessando os URLs do endpoint como esta:

![Imagem da tela de_login_django](./readme_images/login-django.png?raw=true "Imagem da tela inicial da API")

## Autenticação

### Obtenção de token JWT

`GET /login/`
~~~~bash
    curl -X POST -H "Content-Type: application/json" -d '{"cpf": "08360313938", "password": "teste123"}' http://localhost:8000/login/
~~~~

### Resposta de login inválido

~~~json
{"detail":"Usuário e/ou senha incorreto(s)"}
~~~~

### Resposta de login válido
 
~~~json
{
  "refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1OTYyMzAxMSwiaWF0IjoxNjU5NTM2NjExLCJqdGkiOiIzMzVmNmQ3NDQ0YTM0MjBmYjhkMTM2ZDk4MWM5YjFkMiIsInVzZXJfaWQiOjF9.q49hG3k5NjG51xJQFZSLZ1w1aOHXY9YdLuNmK1LgcUo",
  "access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5NjIzMDExLCJpYXQiOjE2NTk1MzY2MTEsImp0aSI6IjBjODM3NTkzNjhkZTRlY2U4MzBlYzc2Y2RjZjRlOTViIiwidXNlcl9pZCI6MX0.pEC0PF4ErBOJhh40bqnSczEi_O5i8QcpanGoLeyxhzY"
}
~~~~

Então, basicamente, na resposta são retornados dois tokens.

Depois disso, você armazenará o token de acesso (**access**) e o token de atualização (**refresh**) no lado do cliente, geralmente no localStorage.

Para acessar as visualizações protegidas no back-end (ou seja, os endpoints da API que exigem autenticação), você deve incluir o token de acesso no cabeçalho de todas as solicitações (como será feito nos próximos exemplos).


## Validação de token

`POST /token/validar/`

dados JSON: **token**

~~~~bash
    curl -H 'Content-Type: application/json' -d '{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5NjIzMDExLCJpYXQiOjE2NTk1MzY2MTEsImp0aSI6IjBjODM3NTkzNjhkZTRlY2U4MzBlYzc2Y2RjZjRlOTViIiwidXNlcl9pZCI6MX0.pEC0PF4ErBOJhh40bqnSczEi_O5i8QcpanGoLeyxhzY"}' -X POST http://localhost:8000/token/validar/
~~~~

Se o token for válido, a resposta será vazia, com **status HTTP 200**.
~~~json
{}
~~~~

Se o token estiver expirado, a resposta terá **status HTTP 401**.
~~~json
{
"detail": "O token é inválido ou expirado",
"code": "token_not_valid"
}
~~~~

### Token refresh

O token retornado expira, mas podemos conseguir um novo token para o usuário através do **refresh**

`GET /login/refresh/`
~~~~bash
curl -H 'Content-Type: application/json' -d '{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5NjIzMDExLCJpYXQiOjE2NTk1MzY2MTEsImp0aSI6IjBjODM3NTkzNjhkZTRlY2U4MzBlYzc2Y2RjZjRlOTViIiwidXNlcl9pZCI6MX0.pEC0PF4ErBOJhh40bqnSczEi_O5i8QcpanGoLeyxhzY"}' -X POST http://localhost:8000/login/refresh/
~~~~


### Validação de login

Atendendo a um requisito, o login pode ser validado através deste endpoint.

`GET /login/validar/`
~~~~bash
curl -H 'Content-Type: application/json' -d '{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5NjIzMDExLCJpYXQiOjE2NTk1MzY2MTEsImp0aSI6IjBjODM3NTkzNjhkZTRlY2U4MzBlYzc2Y2RjZjRlOTViIiwidXNlcl9pZCI6MX0.pEC0PF4ErBOJhh40bqnSczEi_O5i8QcpanGoLeyxhzY"}' -X POST http://localhost:8000/login/refresh/
~~~~

Respota para login válido: **status 200**
~~~json
{
    "statusCode": 200,
    "body": {
        "message": "Login válido",
        "valid": true
    }
}
~~~

Respota para login inválido: **status 200**
~~~json
{
    "statusCode": 200,
    "body": {
        "message": "Login inválido",
        "valid": false
    }
}
~~~

Respota token inválido: status 401
~~~json
{
"detail": "O token informado não é válido para qualquer tipo de token",
"code": "token_not_valid",
    "messages": [
        {
        "token_class": "AccessToken",
        "token_type": "access",
        "message": "O token é inválido ou expirado"
        }
    ]
}
~~~

### Revendedor

#### Lista de revendedores

`GET /api/revendedor/`
~~~bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5NjIzMDExLCJpYXQiOjE2NTk1MzY2MTEsImp0aSI6IjBjODM3NTkzNjhkZTRlY2U4MzBlYzc2Y2RjZjRlOTViIiwidXNlcl9pZCI6MX0.pEC0PF4ErBOJhh40bqnSczEi_O5i8QcpanGoLeyxhzY" http://localhost:8000/api/revendedor/
~~~

Exemplo de retorno
~~~json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "teste@boticario.com.br",
            "first_name": "Nome",
            "last_name": "Teste",
            "cpf": "47352849076",
            "nome_completo": "Nome Teste"
        },
        {
            "email": "teste@boticario.com",
            "first_name": "",
            "last_name": "",
            "cpf": "08360313938",
            "nome_completo": "Nome Teste2"
        }
    ]
}
~~~

#### Cadastro de revendedores

`POST /api/revendedor/`

Exemplo de JSON
~~~json
{
    "email": "teste@boticario.com.br",
    "first_name": "Nome",
    "last_name": "Teste",
    "cpf": "16395482033",
    "nome_completo": "Nome Teste"
}
~~~~

cURL Cadastro
~~~~bash
  curl --location --request POST 'http://localhost:8000/api/revendedor/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5NjMwNDYzLCJpYXQiOjE2NTk1NDQwNjMsImp0aSI6ImNiOGI3MWNkYzAwZDRmNTI4ZjVlNGQyOGMzNWM0MzZhIiwidXNlcl9pZCI6MX0.MiuOQmY49GZqo97F57dNMeSIo3koKWzWN9HOaHFwlxU' \
--header 'Content-Type: application/json' \
--data-raw '{
    "nome_completo": "Nome Teste",
    "cpf": "17415458036",
    "email": "teste@boticario.com.br",
    "password": "TB-teste-123"
}'
~~~~

### Compra

#### Lista de compras

`GET /api/compra/`
~~~bash
curl --location --request GET 'http://localhost:8000/api/compra/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5NjMwNDYzLCJpYXQiOjE2NTk1NDQwNjMsImp0aSI6ImNiOGI3MWNkYzAwZDRmNTI4ZjVlNGQyOGMzNWM0MzZhIiwidXNlcl9pZCI6MX0.MiuOQmY49GZqo97F57dNMeSIo3koKWzWN9HOaHFwlxU' \
--header 'Content-Type: application/json'
~~~

#### Cadastro de compras

`POST /api/compra/`

Exemplo de JSON
~~~json
{
  "revendedor": "153.509.460-56",
  "codigo": "123",
  "data": "2022-01-01",
  "valor": "2000"
}
~~~~

cURL Cadastro
~~~~bash
curl --location --request POST 'http://localhost:8000/api/compra/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU5NjMwNDYzLCJpYXQiOjE2NTk1NDQwNjMsImp0aSI6ImNiOGI3MWNkYzAwZDRmNTI4ZjVlNGQyOGMzNWM0MzZhIiwidXNlcl9pZCI6MX0.MiuOQmY49GZqo97F57dNMeSIo3koKWzWN9HOaHFwlxU' \
--header 'Content-Type: application/json' \
--data-raw '{
    "revendedor": "153.509.460-56",
    "codigo": "123",
    "data": "2022-01-01",
    "valor": "2000"
}'
~~~~

<br>
<br>
<hr>

# Testes

Os testes podem ser rodados dentro do contâiner do sistema.
Pode-se rodá-los com o comando:

```shell
docker container exec -ti sistema python manage.py test
```

# Logs
Os logs são salvos automaticamente na pasta **/logs** na raiz da aplicação.
No momento eles estão definidos com o nível <span style="color:ORANGE">*WARNING*</span>.

# Produção

**Este não é o foco deste desenvolvimento**, mas está disponível um ambiente para produção, utilizando o **Guicorn**.

Pode-se criar a imagem com o comando:

~~~bash
docker run -it -p 8020:8020 cashback_prod
~~~