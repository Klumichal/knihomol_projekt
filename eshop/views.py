from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.template.response import TemplateResponse
from eshop.models import Product, Cart, ProductReview, HelpdeskContact, Category
from eshop.forms import ProductReviewForm, HeldeskContactForm, RegistrationForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views.generic import TemplateView, FormView, CreateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormMixin

class LoginView(FormView, TemplateView):
    template_name = "login.html"
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        username= request.POST.get("username")
        password= request.POST.get("password")
        user= authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Přihlášnení v pořádku")
            return  redirect("homepage")

        messages.error(request, "Neplatné přihlašovací údaje")
        return redirect("login")

class LogoutView(View):

    def get(self, request, *args,**kwargs):
        logout(request)
        messages.success(request, "Odhlášení bylo úspěšné")
        return redirect("homepage")

class HomepageView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        category = self.request.GET.get("category")

        categories = Category.objects.all()

        if category:
            products = Product.objects.filter(category=category)
        else:
            products = Product.objects.all()

        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            cart = None

        context.update({
            "categories": categories,
            "products": products,
            "cart": cart
        })

        return context



@login_required
def add_to_cart_view(request, item_pk):
    product = get_object_or_404(Product, pk=item_pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    return redirect(request.META.get("HTTP_REFERER", "homepage"))

@login_required
def remove_from_cart_view(request, item_pk):
    product = get_object_or_404(Product, pk=item_pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.remove(product)
    return redirect(request.META.get("HTTP_REFERER", "homepage"))

@login_required
def cart_view(request, pk):
    cart = get_object_or_404(Cart, pk=pk, user=request.user)
    context = {
        "cart": cart
    }
    return TemplateResponse(request, "cart.html", context=context)

class RegistrationView(FormMixin, TemplateView):
    template_name = "registration.html"
    form_class = RegistrationForm

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Účet byl vytvořen!")
            return redirect("login")
        messages.error(request, "Nastala chyba")
        return TemplateResponse(request, "registration.html", context={"form": form})


class ListProductReviewView(LoginRequiredMixin, FormView):
    template_name = "product_reviews.html"
    form_class = ProductReviewForm

    def get_initial(self):
        product = self.get_object()
        return {"product": product, "user": self.request.user}

    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs["product_pk"])

    def get_context_data(self, **kwargs):
        context = super(ListProductReviewView, self).get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs["product_pk"])
        user = self.request.user
        context.update({
            "product": product,
            "cart": user.cart

        })
        return context

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs["product_pk"])
        user = self.request.user

        form_data = {
            "user": user.pk,
            "product": product.pk,
            "text": request.POST.get("text"),
            "score": request.POST.get("score")
        }

        bounded_form = ProductReviewForm(data=form_data)
        if not bounded_form.is_valid():
            return JsonResponse(status=400, data={"message": "invalid_data"})

        ProductReview.objects.create(
            user=bounded_form.cleaned_data["user"],
            product=bounded_form.cleaned_data["product"],
            text=bounded_form.cleaned_data["text"],
            score=bounded_form.cleaned_data["score"]
        )

        return self.get(request, *args, **kwargs)

class DeleteProductReview(View):

    def get(self, request, pk, *args, **kwargs):
        product_review = get_object_or_404(ProductReview, pk=pk)
        product_review.delete()
        return redirect(request.META.get("HTTP_REFER", "homepage"))


class HelpdeskContactView(CreateView):
    template_name = "contact.html"
    form_class = HeldeskContactForm
    model = HelpdeskContact
    success_url= reverse_lazy ("homepage")

    def get_context_data(self, **kwargs):
        context = super(HelpdeskContactView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            cart = None

        context.update({
            "cart": cart
        })
        return context