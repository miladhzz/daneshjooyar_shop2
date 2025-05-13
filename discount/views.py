from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import DiscountCode
from core.logger import logger


@login_required
def apply_discount(request):
    try:
        order_price = int(request.GET.get('order_price', 0))
        discount_code = request.GET.get('discount_code', "")

        new_price = order_price
        total_discount = 0

        try:
            discount = DiscountCode.objects.active().get(code=discount_code)
            new_price = discount.get_discount(order_price)
            total_discount = order_price - new_price
            
            logger.info(f"Discount code applied - Code: {discount_code} - Discount: {total_discount} - Final price: {new_price}")
        except DiscountCode.DoesNotExist:
            logger.warning(f"Invalid discount code: {discount_code}")
        except Exception as e:
            logger.error(f"Error applying discount code {discount_code}: {str(e)}")

        return JsonResponse({'new_price': new_price, 'total_discount': total_discount})
    except Exception as e:
        logger.error(f"General error in applying discount: {str(e)}")
        return JsonResponse({'new_price': order_price, 'total_discount': 0})
