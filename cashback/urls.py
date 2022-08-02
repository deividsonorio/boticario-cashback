"""cashback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenVerifyView
import revendedor.views as views

router = routers.DefaultRouter()
router.register(r'api/revendedor', views.RevendedoresViewSet)
router.register(r'api/grupo', views.GroupViewSet)
router.register(r'api/compra', views.CompraViewSet)


urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/validar/', TokenVerifyView.as_view(), name='valida_token'),
    path('login/validar/', views.ValidaLoginRevendedor.as_view(), name='revendedor_valida_login'),
    path('api/revendedor/cashback', views.AcumuladoCashback.as_view(), name='revendedor_cashback'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls))
]
