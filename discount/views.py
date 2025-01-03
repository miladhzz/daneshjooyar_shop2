from django.http import JsonResponse
from discount.models import DiscountCode
from django.contrib.auth.decorators import login_required


@login_required
def apply_discount(request):
    order_price = int(request.GET.get('order_price', 0))
    discount_code = (request.GET.get('discount_code', ""))

    new_price = order_price
    discount_price = 0
    try:
        discount = DiscountCode.objects.get(code=discount_code)
        new_price = discount.get_discount(order_price)
        discount_price = order_price - new_price
    except DiscountCode.DoesNotExist:
        pass

    return JsonResponse({'new_price': new_price, 'total_discount': discount_price})
