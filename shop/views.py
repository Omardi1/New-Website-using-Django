from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.views.generic.base import View

from shop.forms import CartAddProductForm
from shop.models import Cart, Category, Product

from .forms import ProductForm


def index(request):
    products = Product.objects.all()
    form = CartAddProductForm
    q = request.GET.get("q")
    request.session["nom"] = "CasAgro"
    request.session.get("nom")
    del request.session["nom"]
    if q:
        products = Product.objects.filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(category__name__icontains=q)
        )
    context = {"title": "Bienvenue chez vous", "products": products, "form": form}
    return render(request, "index.html", context)


class ProductList(View):
    template_name = "shop/product_list.html"

    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        q = request.GET.get("q")
        selected_category = request.GET.get(
            "category"
        )  # Récupérer la catégorie sélectionnée

        if selected_category:
            products = products.filter(
                category__id=selected_category
            )  # Filtrer les produits par catégorie

        if q:
            products = products.filter(
                Q(name__icontains=q)
                | Q(description__icontains=q)
                | Q(category__name__icontains=q)
            )

        return render(
            request,
            self.template_name,
            {
                "products": products,
                "categories": categories,
                "selected_category": selected_category,  # Passer la catégorie sélectionnée au template
            },
        )


class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "shop/product_detail.html"
    # def get(self, request):
    #     return render(request, self.template_name, {"product": product})

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context["cart_product_form"] = CartAddProductForm()
        return context


def Product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "detail.html", context={"product": product})


def new_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = ProductForm()
        context = {"form": form}
    return render(request, "new_product.html", context)


def update_product(request, slug):
    context = {}
    product = get_object_or_404(Product, slug=slug)
    form = ProductForm(request.POST, instance=product)
    if form.is_valid():
        form.save()
        return redirect("index")
    context["form"] = form
    return render(request, "update_product.html", context)


def delete_product(request, slug):
    contex = {}
    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        product.delete()
        return redirect("index")
    return render(request, "shop/delete_product.html", contex)


@require_POST
def cart_add(request, slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=slug)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        cart.add(
            product=product,
            quantity=cleaned_data["quantity"],
            override_qauntity=cleaned_data["override"],
        )
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
        item["update_quantity_form"] = CartAddProductForm(
            initial={"quantity": item["quantity"], "override": True}
        )

    return render(request, "cart/cart_detail.html", {"cart": cart})
