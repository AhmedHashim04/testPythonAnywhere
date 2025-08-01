from decimal import Decimal
from .utils import generate_invoice_pdf
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View, FormView, UpdateView, DeleteView
from product.models import Product
from cart.cart import Cart
from .forms import AddressForm, OrderCreateForm
from .models import Address, Order, OrderItem
from allauth.socialaccount.providers import registry

from django.utils.http import urlencode


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "order/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "order/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "order/create_order.html"
    success_url = reverse_lazy("order:order_list")



    def form_valid(self, form):
        
        cart = Cart(self.request)
        if len(cart) == 0:
            form.add_error(None, "Your cart is empty.")
            return super().form_invalid(form)

        try:
            with transaction.atomic():
                order = self._create_order_object(form, cart)

                self._create_order_items(order, cart)
                self.object = order

            self._invoice_generation(order)
            self._cleanup_session(cart)
            messages.success(
                self.request,
                _("Your order has been placed successfully. "
                "Your invoice is being generated and will be available shortly."),
            )

        except Exception as e:
            # logger.exception("Order processing failed")
            form.add_error(None, _("Error processing your order: %(error)s") % {'error': str(e)})
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_initial(self):

        profile = getattr(self.request.user, 'profile', None)
        initial = {
        }
        if profile:
            initial.update({
                'full_name': self.request.user.get_full_name() or self.request.user.username,
                'governorate': profile.governorate,
                'phone': profile.phone,
            })
        return initial


    def _create_order_object(self, form, cart):
        order = form.save(commit=False)
        order.user = self.request.user
        order.shipping_cost = order.calculate_shipping_cost()

        order.shipping_option = form.cleaned_data['shipping_option']

        get_total_price_after_discount = cart.get_total_price_after_discount()
        order.total_price = max(
            (get_total_price_after_discount + order.shipping_cost).quantize(Decimal("0.01")),
            Decimal("0.00"),
        )
        order.save()
        return order

    def _create_order_items(self, order, cart):
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["price"],
                discount=item["discount"],
            )

    def _invoice_generation(self, order):
        pdf_content = generate_invoice_pdf(order)
        if pdf_content:
            order.invoice_pdf.save(f"invoice_{order.id}.pdf", ContentFile(pdf_content))
            order.save()

    def _cleanup_session(self, cart):
        """Clean session data after successful order"""
        cart.clear()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart(self.request)
        if "form" not in context:
            context["form"] = self.get_form()
        return context

    def get_form(self, form_class=None):
        
        form_class = form_class or self.get_form_class()
        if self.request.method == "POST":
            return form_class(self.request.POST, user=self.request.user)
        return form_class(user=self.request.user, initial=self.get_initial())

class OrderCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = Order.objects.filter(pk=pk, user=request.user).first()
        if order and hasattr(order, "status"):
            order.update_status("cancelled")
        return HttpResponseRedirect(reverse("order:order_detail", args=[order.pk]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.object
        return context

class AddressEditView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["edit"] = True
        return context

    template_name = "order/address_list_create.html"
    def get_success_url(self):
        messages.success(self.request, _("Address updated successfully."))
        return reverse("order:address_list_create")
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    def form_valid(self, form):
        address = form.save(commit=False)
        if address.is_default:
            Address.objects.filter(user=self.request.user, is_default=True).exclude(pk=address.pk).update(is_default=False)
        address.save()
        return super().form_valid(form)

class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = "order/address_confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, _("Address deleted successfully."))
        return reverse("order:address_list_create")

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

class AddressSetDefaultView(LoginRequiredMixin, View):
    def post(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
        address.is_default = True
        address.save()
        messages.success(request, _("Default address set successfully."))
        return redirect("order:address_list_create")
    def get(self, request, pk):
        return self.post(request, pk)

class AddressUnsetDefaultView(LoginRequiredMixin, View):
    def post(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        address.is_default = False
        address.save()
        messages.success(request, _("Default address unset successfully."))
        return redirect("order:address_list_create")
    def get(self, request, pk):
        return self.post(request, pk)

class AddressListCreateView(LoginRequiredMixin, FormView, ListView):
    template_name = "order/address_list_create.html"
    form_class = AddressForm
    success_url = reverse_lazy("order:create_order")

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get_initial(self):
        profile = getattr(self.request.user, 'profile', None)
        initial = {
        }
        if profile:
            initial.update({
                'governorate': profile.governorate,
                'address_line': profile.address,
            })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["addresses"] = self.get_queryset()
        if "form" not in context:
            context["form"] = self.get_form()
        return context

    def get_form(self, form_class=None):
        if self.request.method in ("POST", "PUT"):
            return self.form_class(self.request.POST)
        return self.form_class(initial=self.get_initial())

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user

        if address.is_default:
            Address.objects.filter(user=self.request.user, is_default=True).update(is_default=False)

        address.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


# def get_google_provider():
#     return registry.providers.get("google")


class OrderNowCreateView(CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "order/create_order.html"
    success_url = reverse_lazy("order:order_list")

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     provider = get_google_provider()
        #     if provider:
        #         login_url = provider.get_login_url(request)
        #         return redirect(login_url)

        self.product = get_object_or_404(Product, slug=kwargs.get("slug"))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        
        if not self.product:
            form.add_error(None, "Your there is no product. ")
            return super().form_invalid(form)

        try:
            with transaction.atomic():
                order = self._create_order_object(form)

                self._create_order_items(order)
                self.object = order

            self._invoice_generation(order)
            messages.success(
                self.request,
                _("Your order has been placed successfully. "
                "Your invoice is being generated and will be available shortly."),
            )

        except Exception as e:
            form.add_error(None, _("Error processing your order: %(error)s") % {'error': str(e)})
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_initial(self):
        if self.request.user.is_authenticated:
            profile = getattr(self.request.user, 'profile', None)
            initial = {
            }
            if profile:
                initial.update({
                    'full_name': self.request.user.get_full_name() or self.request.user.username,
                    'governorate': profile.governorate,
                    'phone': profile.phone,
                })
            return initial


    def _create_order_object(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.shipping_cost = order.calculate_shipping_cost()

        order.shipping_option = form.cleaned_data['shipping_option']

        get_total_price_after_discount = self.product.price_after_discount
        order.total_price = max(
            (get_total_price_after_discount + order.shipping_cost).quantize(Decimal("0.01")),
            Decimal("0.00"),
        )
        order.save()
        return order

    def _create_order_items(self, order):
        OrderItem.objects.create(
                order=order,
                product=self.product,
                quantity=1,
                price=self.product.price,
                discount=self.product.discount,
            )

    def _invoice_generation(self, order):
        pdf_content = generate_invoice_pdf(order)
        if pdf_content:
            order.invoice_pdf.save(f"invoice_{order.id}.pdf", ContentFile(pdf_content))
            order.save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["product"]  = self.product
        if "form" not in context:
            context["form"] = self.get_form()
        return context

    def get_form(self, form_class=None):
        
        form_class = form_class or self.get_form_class()
        if self.request.method == "POST":
            return form_class(self.request.POST, user=self.request.user)
        return form_class(user=self.request.user, initial=self.get_initial())
    

