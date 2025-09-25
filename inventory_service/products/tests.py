import json
from graphene_django.utils.testing import GraphQLTestCase

class MyFancyTestCase(GraphQLTestCase):
    GRAPHQL_URL = "http://localhost:8000/products/gql"

    def test_create_product_m(self):
        response = self.query(
            '''
            mutation CreateProduct {
                createProduct(
                    code: "j"
                    name: "j"
                    price: 2
                    category: "{\\"a\\":{\\"b\\":\\"c\\"}}"
                ) {
                    product {
                        id
                        name
                        code
                        category
                        price
                        createdAt
                        updatedAt
                    }
                }
            }
            ''',
            operation_name='CreateProduct'
        )

        # content = json.loads(response.content)  

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)



    def test_query_all_products_q(self):
        self.query(
            '''
            mutation CreateProduct {
                createProduct(
                code: "j"
                name: "j"
                price: 2
                category: "{\\"a\\":{\\"b\\":\\"c\\"}}"
                ) {
                    product {
                        id
                        name
                        code
                        category
                        price
                        createdAt
                        updatedAt
                    }
                }
            }
            ''',
            operation_name='CreateProduct'
        )

        response = self.query(
            '''
            query AllProducts {
                allProducts {
                    id
                    name
                    code
                    category
                    price
                    createdAt
                    updatedAt
                }
            }
            ''',
            operation_name='AllProducts',
        )

        content = json.loads(response.content)        

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)


    def test_query_product_by_category_q(self):
        self.query(
            '''
            mutation CreateProduct {
                createProduct(
                    code: "j"
                    name: "j"
                    price: 2
                    category: "{\\"a\\":{\\"b\\":\\"c\\"}}"
                ) {
                    product {
                        id
                        name
                        code
                        category
                        price
                        createdAt
                        updatedAt
                    }
                }
            }
            ''',
            operation_name='CreateProduct'
        )

        response = self.query(
            '''
            query ProductByCategory {
                productByCategory(category: "b") {
                    id
                    name
                    code
                    category
                    price
                    createdAt
                    updatedAt
                }
            }
            ''',
            operation_name='ProductByCategory',
        )
        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)

