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
import custom_configs.schema as custom_configs


urlpatterns = [
    path('admin/', admin.site.urls),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('customers/gql', GraphQLView.as_view(graphiql=True, schema=customers.schema)),
    path('orders/gql', GraphQLView.as_view(graphiql=True, schema=orders.schema)),
    path('products/gql', GraphQLView.as_view(graphiql=True, schema=products.schema)),
    path('configs/gql', GraphQLView.as_view(graphiql=True, schema=custom_configs.schema)),
    path('api/customers/gql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=customers.schema))),
    path('api/orders/gql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=orders.schema))),
    path('api/products/gql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=products.schema))),
    path('api/configs/gql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=custom_configs.schema))),
]
