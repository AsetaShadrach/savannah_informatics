import os
import graphene
from graphene_django import DjangoObjectType
from customers.models import Customer
from custom_configs.models import CustomConfigs
import requests
from dotenv import load_dotenv

load_dotenv()

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class LoginType(graphene.ObjectType):
    access_token = graphene.String()
    expires_in = graphene.Int()
    refresh_expires_in = graphene.Int()
    refresh_token= graphene.String()
    token_type = graphene.String()
    session_state = graphene.String()
    scope = graphene.String()


class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    customer_by_phone_number= graphene.Field(CustomerType, phone_number=graphene.String())
    customer_by_customer_id  = graphene.List(CustomerType, customer_id=graphene.String())
    customer_by_date = graphene.List(CustomerType, date_from=graphene.Date(), date_to=graphene.Date())

    def resolve_all_customers(root, info):
        return ( Customer.objects.all()
        )

    def resolve_customer_by_phone_number(root, info, phone_number):
        return (
            Customer.objects.get(phone_number=phone_number)
        )

    def resolve_customer_by_customer_id(root, info, customer_id):
        return (
            Customer.objects.filter(id=customer_id)
        )

    def resolve_customer_by_date(root, info, date_from , date_to):
        return (
            Customer.objects.filter(created_at__gte=date_from , created_at__lte=date_to )
        )



class CreateCustomer(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required= True)
        last_name = graphene.String(required= True)
        phone_number = graphene.String(required= True)
        email = graphene.String(required= True)
        username = graphene.String(required= True)
        password = graphene.String(required= True)
    
    customer  = graphene.Field(CustomerType)

    def mutate(self, info , first_name, last_name, phone_number , email, username, password):
        # Assuming  all customers are from Kenya 

        minimum_password_length  = CustomConfigs.objects.get(name='minimum_password_length').value

        if len(password) <= int(minimum_password_length) :
            raise Exception (f"Password length should be greater that {minimum_password_length} characters")
        customer = Customer(first_name=first_name, last_name=last_name , phone_number=phone_number , email=email)
        customer.save()

        KEYCLOAK_USERS_ENDPOINT = os.getenv('KEYCLOAK_USERS_ENDPOINT')
        KEYCLOAK_ADMIN_LOGIN = os.getenv('KEYCLOAK_LOGIN_ENDPOINT')        

        login_body = {
            "grant_type": "client_credentials",
            "client_id": CustomConfigs.objects.get(name='KEYCLOAK_ADMIN_CLIENT_ID').value,
            "client_secret": CustomConfigs.objects.get(name='KEYCLOAK_ADMIN_CLIENT_SECRET').value   
        }

        resp = requests.post(KEYCLOAK_ADMIN_LOGIN, data=login_body, headers= {
            'Content-Type': 'application/x-www-form-urlencoded'
        } )

        if resp.status_code !=200:
            return Exception(resp.json())

        keycloak_body = {
            "username": username,
            "emailVerified": True,
            "email": customer.email,
            "firstName": customer.first_name,
            "lastName": customer.last_name,
            "enabled": True,
            "credentials" : [
                        {
                            "type" : "password",
                            "value" : password
                        }
                    ]
                }
        token = resp.json()["access_token"]

        resp = requests.post(KEYCLOAK_USERS_ENDPOINT, json=keycloak_body, headers={
            "Authorization" : f"Bearer {token}",
        })

        if resp.status_code == 201:
            print("User creation successful")
            return CreateCustomer(customer=customer)
        else:
            print("Exception happened  --------> ")
            return Exception(f"{resp.status_code} --> {resp.json()}")


class UpdateCustomer(graphene.Mutation):
    class Arguments:
        id =  graphene.Int(required = True)
        first_name = graphene.String()
        last_name = graphene.String()
        phone_number = graphene.String()
        email = graphene.String()
        
    customer  = graphene.Field(CustomerType)

    def mutate(self, info , id , first_name = None , last_name= None, email = None , phone_number = None  ):
        
        try:
            customer = Customer.objects.get(pk= id)
        except:
            raise Exception("Not found")
        
        if first_name is not None:
            customer.first_name = first_name
        if last_name is not None:
            customer.last_name = last_name
        if email is not None:
            customer.email = email
        if phone_number is not None:
            customer.phone_number = phone_number

        customer.save()
        return UpdateCustomer(customer=customer)


class LoginCustomer(graphene.Mutation):
    class Arguments:
        username = graphene.String(required= True)
        password = graphene.String(required= True)
    
    token  = graphene.Field(LoginType)

    def mutate(self, info , username, password):
        login_body = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": os.getenv('KEYCLOAK_ADMIN_CLIENT_ID'),
            "client_secret": os.getenv('KEYCLOAK_ADMIN_CLIENT_SECRET')     
        }
        KEYCLOAK_USER_LOGIN = os.getenv('KEYCLOAK_LOGIN_ENDPOINT')

        resp = requests.post(KEYCLOAK_USER_LOGIN, data=login_body, headers= {
            'Content-Type': 'application/x-www-form-urlencoded'
        } )

        if resp.status_code !=200:
            return Exception(resp.json())
        else:
            return LoginCustomer(token = resp.json() )
        

class Mutation(graphene.ObjectType):
    update_customer = UpdateCustomer.Field()
    create_customer = CreateCustomer.Field()
    # login_customer = LoginCustomer.Field()


schema = graphene.Schema(query=Query, mutation = Mutation)