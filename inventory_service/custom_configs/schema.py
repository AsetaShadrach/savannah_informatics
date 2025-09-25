import graphene
from graphene_django import DjangoObjectType
from custom_configs.models import CustomConfigs
from django.db.models import Sum, Count

class CustomConfigsType(DjangoObjectType):
    class Meta:
        model = CustomConfigs


class Query(graphene.ObjectType):
    all_custom_configs = graphene.List(CustomConfigsType)
    custom_config_by_name = graphene.List(CustomConfigsType, name=graphene.String())
    

    def resolve_all_custom_configs(root, info):
        return ( 
            CustomConfigs.objects.all()
        )

    def resolve_custom_config_by_name(root, info, name):
        return (
            CustomConfigs.objects.filter(name__icontains=name)
        )
    

class CreateCustomConfig(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        value = graphene.String(required=True)
    
    custom_config  = graphene.Field(CustomConfigsType)

    def mutate(self, info , name, value ):
        custom_config = CustomConfigs(name=name, value=value )
        custom_config.save()
        print("Successfuly created custom_config : ", custom_config)
        return CreateCustomConfig(custom_config=custom_config)


class UpdateCustomConfig(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required =True)
        name = graphene.String()
        value = graphene.String()
    
    custom_config  = graphene.Field(CustomConfigsType)

    def mutate(self, info , id , name=None , value = None ):
        
        try:
            custom_config = CustomConfigs.objects.get(pk= id)
        except:
            raise Exception("Not found")
        
        if name is not None:
            custom_config.name = name
        if value is not None:
            custom_config.value = value

        custom_config.save()
        return UpdateCustomConfig(custom_config=custom_config)


class Mutation(graphene.ObjectType):
    create_custom_config = CreateCustomConfig.Field()
    update_custom_config = UpdateCustomConfig.Field()

  

schema = graphene.Schema(query=Query, mutation = Mutation)