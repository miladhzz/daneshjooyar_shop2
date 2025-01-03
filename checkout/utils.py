from checkout.models import Order, OrderProduct
from . import models
from discount.models import DiscountCode


def save_order_user(cart, request):
    discount = get_discount(request, cart)
    order = Order.objects.create(
        user=request.user,
        note=request.POST.get('note'),
        total_price=discount.get('total_price'),
        discount_id=discount.get('discount_id'),
        discount_code=discount.get('discount_code'),
        total_discount=discount.get('total_discount'),
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
    discount = get_discount(request, cart)
    order = Order.objects.create(
        user=request.user,
        note=request.POST.get('note'),
        total_price=discount.get('total_price'),
        discount_id=discount.get('discount_id'),
        discount_code=discount.get('discount_code'),
        total_discount=discount.get('total_discount'),
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


def get_discount(request, cart):
    discount_code = request.POST.get('discount_code')
    order_price = cart.get_total_price

    result = {
        'total_price': order_price,
        'total_discount': 0,
        'discount_id': None,
        'discount_code': discount_code
    }
    if not discount_code:
        return result

    try:
        discount = DiscountCode.objects.get(code=discount_code)
        result['discount_id'] = discount.id
        result['total_price'] = new_price = discount.get_discount(order_price)
        result['total_discount'] = order_price - new_price
    except DiscountCode.DoesNotExist:
        pass

    return result
