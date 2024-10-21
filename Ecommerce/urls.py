
#from shop.views import index, Product_detail
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt  # Import for CSRF exemption
from shop.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("shop.urls")),
    path('utilisateurs/', include("utilisateurs.urls")),
    path('orders', include("orders.urls")),
    path('cart', include("cart.urls")),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


