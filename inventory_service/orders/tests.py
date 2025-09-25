import json
from graphene_django.utils.testing import GraphQLTestCase

class MyFancyTestCase(GraphQLTestCase):
    GRAPHQL_URL = "http://localhost:8000/orders/gql"

    def test_create_order_m(self):
        response = self.query(
            '''
            mutation CreateOrder {
                createOrder(
                    customerId: 1 
                    orderDetails: "{\\"a\\":1,\\"b\\":2}"
                ) {                
                    order {
                        id
                        orderRef
                        orderDetails
                        total
                        status
                        createdAt
                        updatedAt
                    }
                }
            }
            ''',
            operation_name='CreateOrder',
            # input_data={'my_field': 'foo', 'other_field': 'bar'}
        )

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)



    def test_query_all_orders_q(self):
        self.query(
            '''
            mutation CreateOrder {
                createOrder(
                    customerId: 1 
                    orderDetails: "{\\"a\\":1,\\"b\\":2}"
                ) {
                    order {
                        id
                        orderRef
                        orderDetails
                        total
                        status
                        createdAt
                        updatedAt
                    }
                }
            }
            ''',
            operation_name='CreateOrder',
            # input_data={'my_field': 'foo', 'other_field': 'bar'}
        )

        response = self.query(
            '''
            query AllOrders {
                allOrders {
                    id
                    orderRef
                    orderDetails
                    total
                    status
                    createdAt
                    updatedAt
                }
            }
            ''',
            operation_name='AllOrders',
        )

        content = json.loads(response.content)        

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
