
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from django.views.decorators.http import require_POST
from django.views.generic.base import View
from shop.forms import CartAddProductForm
from django.db.models import Q
from shop.models import Cart, Product, Category


def index(request):
    products = Product.objects.all()
    form = CartAddProductForm
    context = {"title": "Bienvenue chez vous", "products": products, "form": form} 
    return render(request, 'index.html',  context)



class ProductList(View):
    template_name = 'shop/product_list.html'

    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        q = request.GET.get("q")
        request.session["nom"] = "CasAgro"
        request.session.get("nom")
        del request.session["nom"]
        if q:
            products = Product.objects.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
            )
        return render(request, self.template_name, {"products": products, "categories": categories, })


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_details.html'
    # def get(self, request):
    #     return render(request, self.template_name, {"product": product})

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context["cart_product_form"] = CartAddProductForm()
        return context    

def Product_detail(request, slug):
    product= get_object_or_404(Product, slug=slug)
    return render(request, 'detail.html', context={"product": product})


@require_POST
def cart_add(request, slug):
    cart = Cart.object
    product = get_object_or_404(Product, slug=slug)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        cart.add(product=product,
                 quantity=cleaned_data["quantity"], override_qauntity=cleaned_data["override"])
        return redirect("cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart_detail")


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={"quantity": item["quantity"], "override": True})

    return render(request, "cart/cart_detail.html", {"cart": cart})
