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
        models.Cartobjects.get(user_id=user_id, product_id=product_id).delete()
    except models.Cart.DoesNotExist:
        pass


def sync_cart_session_to_db(request, cart):
    user_id = request.user.id
    session_key = request.session.session_key

    models.Cart.objects.filter(user_id=user_id).exclude(product_id__in=cart.product_ids).delete()

    for item in cart:
        cart_db, created = models.Cart.objects.get_or_create(
            user_id=user_id,
            product_id=item['product_id'],
            defaults={
                'quantity': item['quantity'],
                'session_key': session_key
            }
        )
        if not created:
            cart_db.quantity = item['quantity']
            cart_db.session_key = session_key
            cart_db.save()


def sync_cart_db_to_session(request, cart):
    user_id = request.user.id
    session_key = request.session.session_key

    if models.Cart.objects.filter(user_id=user_id, session_key=session_key).exists():
        return

    cart_items = models.Cart.objects.filter(user_id=user_id)
    for item in cart_items:
        item.session_key = session_key
        cart.add(product_id=item.product.id,
                 product_price=item.product.price,
                 quantity=item.quantity,
                 update=False)

    models.Cart.objects.bulk_update(cart_items, ['session_key'])
