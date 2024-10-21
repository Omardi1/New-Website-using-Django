import graphene
from graphene_django.types import DjangoObjectType
from .models import Category, Product

# Crée des types GraphQL basés sur tes modèles
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

# Définit les requêtes possibles pour ton schéma
class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)
    all_products = graphene.List(ProductType)
    product = graphene.Field(ProductType, slug=graphene.String(required=True))

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_product(self, info, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return None

# Schéma principal
schema = graphene.Schema(query=Query)
