from checkout.models import Order, OrderProduct
from discount.utils import get_discount


def save_order_user(cart, request):
    discount = get_discount(request, cart)

    order = Order.objects.create(
        user=request.user,
        total_price=discount['total_price'],
        discount_code=discount['discount_code'],
        discount_id=discount['discount_id'],
        total_discount=discount['total_discount'],
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
    discount = get_discount(request, cart)

    order = Order.objects.create(
        user=request.user,
        total_price=discount['total_price'],
        discount_code=discount['discount_code'],
        discount_id=discount['discount_id'],
        total_discount=discount['total_discount'],
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
