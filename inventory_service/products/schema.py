import graphene
from graphene_django import DjangoObjectType
from products.models import Product
from django.db.models import Sum, Count

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class ProductCategorySummaryType(graphene.ObjectType):
    items = graphene.Int()
    price_sum = graphene.Int()

class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    product_by_code = graphene.Field(ProductType, code=graphene.String())
    product_by_category = graphene.List(ProductType, category=graphene.String())
    product_by_name = graphene.List(ProductType, name=graphene.String())
    category_summary = graphene.Field(ProductCategorySummaryType, category=graphene.String())

    def resolve_all_products(root, info):
        return ( 
            Product.objects.all()
        )

    def resolve_product_by_code(root, info, code):
        return (
            Product.objects.get(code=code)
        )

    def resolve_product_by_category(root, info, category):
        return (
            Product.objects.filter(category__icontains=category)
        )

    def resolve_category_summary(root, info, category):    
        return (
            Product.objects.filter(category__icontains=category).aggregate(
            items=Count('id'), price_sum=Sum('price'))
        )

    def resolve_product_by_name(root, info, name):
        return (
            Product.objects.filter(name__icontains=name)
        )
    

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        code = graphene.String(required=True)
        category = graphene.JSONString()
        price = graphene.Int(required= True)
    
    product  = graphene.Field(ProductType)

    def mutate(self, info , name, code, category , price):
        product = Product(name=name, code=code , category=category , price=price)
        product.save()
        print("Successfuly created product : ", product)
        return CreateProduct(product=product)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required =True)
        name = graphene.String()
        code = graphene.String()
        category = graphene.JSONString()
        price = graphene.Int()
    
    product  = graphene.Field(ProductType)

    def mutate(self, info , id , name=None , code = None , category = None , price = None ):
        
        try:
            product = Product.objects.get(pk= id)
        except:
            raise Exception("Not found")
        
        if name is not None:
            product.name = name
        if code is not None:
            product.code = code
        if category is not None:
            product.category = category
        if price is not None:
            product.price = price

        product.save()
        return UpdateProduct(product=product)


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()

  

schema = graphene.Schema(query=Query, mutation = Mutation)