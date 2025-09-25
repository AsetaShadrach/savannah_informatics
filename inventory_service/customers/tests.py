import json
from graphene_django.utils.testing import GraphQLTestCase

class MyFancyTestCase(GraphQLTestCase):
    GRAPHQL_URL = "http://localhost:8000/customers/gql"

    def test_create_customer_m(self):
        response = self.query(
            '''
            mutation CreateCustomer {
                createCustomer(
                    email: "a@b.com"
                    firstName: "fname"
                    lastName: "lname"
                    password: "password"
                    phoneNumber: "254712345678"
                    username: "abc_test"
                ) {
                    customer {
                        id
                        firstName
                        lastName
                        phoneNumber
                        email
                        createdAt
                        updatedAt
                    }
                }
            }
            ''',
            operation_name='CreateCustomer',
            # input_data={'my_field': 'foo', 'other_field': 'bar'}
        )

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)



    def test_query_all_customers_q(self):
        self.query(
            '''
            mutation CreateCustomer {
                createCustomer(
                    email: "a@b2.com"
                    firstName: "fname"
                    lastName: "lname"
                    password: "password"
                    phoneNumber: "254712345678"
                    username: "abc_test2"
                ) {
                    customer {
                        id
                        firstName
                        lastName
                        phoneNumber
                        email
                        createdAt
                        updatedAt
                    }
                }
            }
            ''',
            operation_name='CreateCustomer',
            # input_data={'my_field': 'foo', 'other_field': 'bar'}
        )

        response = self.query(
            '''
            query AllCustomers {
                allCustomers {
                    id
                    firstName
                    lastName
                    phoneNumber
                    email
                    createdAt
                    updatedAt
                }
            }
            ''',
            operation_name='AllCustomers',
        )

        content = json.loads(response.content)        

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)


    def test_update_customer_m(self):
        self.query(
            '''
            mutation CreateCustomer {
                createCustomer(
                    email: "a@b3.com"
                    firstName: "fname"
                    lastName: "lname"
                    password: "password"
                    phoneNumber: "254712345678"
                    username: "abc_test3"
                ) {
                    customer {
                        id
                        firstName
                        lastName
                        phoneNumber
                        email
                        createdAt
                        updatedAt
                    }
                }
            }
            ''',
            operation_name='CreateCustomer',
            # input_data={'my_field': 'foo', 'other_field': 'bar'}
        )

        response = self.query(
            '''
            mutation UpdateCustomer {
                updateCustomer(
                    id:1
                    firstName: "fn2"
                ) {
                    customer {
                        id
                        firstName
                        lastName
                        phoneNumber
                        email
                        createdAt
                        updatedAt
                    }
                }
            }
            ''',
            operation_name='UpdateCustomer',
        )
        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)

