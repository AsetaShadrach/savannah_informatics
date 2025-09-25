import os
import random
import string
import graphene
from graphene_django import DjangoObjectType
from customers.models import Customer
from notification_service.send_email import send_email_via_sendgid_api
from orders.models import Order
from twilio.rest import Client

class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class Query(graphene.ObjectType):
    all_orders = graphene.List(OrderType)
    order_by_reference= graphene.Field(OrderType, order_ref=graphene.String())
    order_by_customer_id  = graphene.List(OrderType, customer_id=graphene.Int())
    order_by_date = graphene.List(OrderType, date_from=graphene.Date(), date_to=graphene.Date())

    def resolve_all_orders(root, info):
        return ( Order.objects.all()
        )

    def resolve_order_by_reference(root, info, order_ref):
        return (
            Order.objects.get(order_ref=order_ref)
        )

    def resolve_order_by_customer_id(root, info, customer_id):
        return (
            Order.objects.prefetch_related('customer').filter(customer__id=customer_id)
        )

    def resolve_order_by_date(root, info, date_from , date_to):
        return (
            Order.objects.filter(created_at__gte=date_from , created_at__lte=date_to )
        )


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.Int(required= True)
        order_details = graphene.JSONString()
    
    order = graphene.Field(OrderType)

    def mutate(self, info , order_details, customer_id):
        # Generate a random string for ref
        # This can be done better e.g hashing strings
        ref =  ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
        
        # Check that the ref does not exist 
        while Order.objects.filter(order_ref =ref):
            ref =  ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

        # Get sum of all products
        total = sum(order_details.values())
        
        customer = Customer.objects.get(pk = customer_id)
        order = Order(order_ref=ref, customer=customer , order_details=order_details, total=total)
        order.save()

        message= f"Order with ref {order.order_ref}. Has been place by {customer.id} at with a total of {order.total}. \n\nOrder details are {order.order_details}"

        # requests.post(
        #     "https://api.sandbox.africastalking.com/version1/messaging/bulk",
        #     headers={
        #         "apikey": os.getenv("AT_API_KEY")
        #     },
        #     json={
        #         "username": "Sandbox",
        #         "message": f"Order Ref {order.order_ref} for KES {order.total} was placed at {order.created_at}",
        #         "senderId": "Sandbox",
        #         "phoneNumbers": [
        #             f"+{order.customer.phone_number}"
        #         ]
        #     }
        # )


        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)

        sms_message = client.messages.create(
            body=f"Order Ref {order.order_ref} for KES {order.total} was placed at {order.created_at}",
            from_="+15078246008",
            to=f"+{order.customer.phone_number}",
        )

        print("Message Body  --> " , sms_message.body)

        send_email_via_sendgid_api(
            [os.getenv("ADMIN_EMAILS_FOR_ORDERS")], 
            f"ORDER {order.order_ref}",
            message,
            "info"
        )

        return CreateOrder(order=order)


class UpdateOrder(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required =True)
        order_details = graphene.JSONString()
    
    order  = graphene.Field(OrderType)

    def mutate(self, info , id , order_details = None  ):
        
        try:
            order = Order.objects.get(pk= id)
        except:
            raise Exception("Not found")
        
        if order_details is not None:
            order.order_details = order_details

        order.save()
        return UpdateOrder(order=order)


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    update_order = UpdateOrder.Field()

schema = graphene.Schema(query=Query, mutation = Mutation)