"""
URL configuration for inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
import customers.schema as customers
import products.schema as products
import orders.schema as orders
from mozilla_django_oidc import views as oidc_views

def login_view(request):
    return render(request, "login.html")

urlpatterns = [
    path('', login_view),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('oidc/', include('mozilla_django_oidc.urls')),
    # path('login/', oidc_views.OIDCAuthenticationRequestView.as_view(), name='login'),
    # path('logout/', oidc_views.OIDCLogoutView.as_view(), name='logout'),
    path("customers/gql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=customers.schema))),
    path('orders/gql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=orders.schema))),
    path("products/gql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=products.schema))),
]
