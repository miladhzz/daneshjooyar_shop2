from checkout.models import Order, OrderProduct
from . import models


def save_order_user(cart, request):
    order = Order.objects.create(
        user=request.user,
        total_price=cart.get_total_price,
        note=request.POST.get('note'),
        different_address=False,
        first_name=request.user.first_name,
        last_name=request.user.last_name,
        mobile=request.user.mobile,
        postal_code=request.user.profile.postal_code,
        address=request.user.profile.address,
        city_id=request.user.profile.city_id,
    )
    for item in cart:
        OrderProduct.objects.create(order=order,
                                    product_id=item['product_id'],
                                    quantity=item['quantity'],
                                    price=item['price'])
    return order


def save_order_different(cart, order_form, request):
    order = Order.objects.create(
        user=request.user,
        total_price=cart.get_total_price,
        note=request.POST.get('note'),
        different_address=True,
        first_name=order_form.cleaned_data['first_name'],
        last_name=order_form.cleaned_data['last_name'],
        mobile=order_form.cleaned_data['mobile'],
        postal_code=order_form.cleaned_data['postal_code'],
        address=order_form.cleaned_data['address'],
        city_id=order_form.cleaned_data['city'],
    )
    for item in cart:
        OrderProduct.objects.create(order=order,
                                    product_id=item['product_id'],
                                    quantity=item['quantity'],
                                    price=item['price'])
    return order


def add_cart_item_to_db(user_id, cart):
    for item in cart:
        cart_db, created = models.Cart.objects.get_or_create(
            user_id=user_id,
            product_id=item['product_id'],
            defaults={
                'quantity': item['quantity']
            }
        )
        if not created:
            cart_db.quantity = item['quantity']
            cart_db.save()


def remove_cart_item_from_db(user_id, product_id):
    try:
        models.Cart.objects.get(user_id=user_id, product_id=product_id).delete()
    except models.Cart.DoesNotExist:
        pass
