from .models import SpecialPrice, DiscountCode
from core import DiscountType
from django.db.models import Q
from core.logger import logger


def get_special_price(product):
    try:
        special_prices = SpecialPrice.objects.active().filter(
            Q(products=product) | Q(categories=product.category)
        ).distinct()

        max_special = {
            'fixed_type': None,
            'fixed': None,
            'percent_type': None,
            'percent': None
        }

        for special in special_prices:
            special_type = special.special_price_type
            special_value = special.special_price_value

            if special_type == DiscountType.FIXED and (max_special['fixed'] is None or special_value > max_special['fixed']):
                max_special['fixed'] = special_value
                max_special['fixed_type'] = special_type

            if special_type == DiscountType.PERCENT and (max_special['percent'] is None or special_value > max_special['percent']):
                max_special['percent'] = special_value
                max_special['percent_type'] = special_type

        return max_special
    except Exception as e:
        logger.error(f"خطا در محاسبه قیمت ویژه برای محصول {product.title}: {str(e)}")
        return {
            'fixed_type': None,
            'fixed': None,
            'percent_type': None,
            'percent': None
        }


def get_discount(request, cart):
    try:
        discount_code = request.POST.get('discount_code')
        order_price = cart.get_total_price

        result = {
            'total_price': order_price,
            'discount_code': discount_code,
            'discount_id': None,
            'total_discount': 0
        }

        if not discount_code:
            return result

        try:
            discount = DiscountCode.objects.active().get(code=discount_code)
            result['discount_id'] = discount.id
            result['total_price'] = new_price = discount.get_discount(order_price)
            result['total_discount'] = order_price - new_price
            
            logger.info(f"اعمال کد تخفیف موفق - کد: {discount_code} - تخفیف: {result['total_discount']} - قیمت نهایی: {new_price}")
        except DiscountCode.DoesNotExist:
            logger.warning(f"کد تخفیف نامعتبر: {discount_code}")
        except Exception as e:
            logger.error(f"خطا در اعمال کد تخفیف {discount_code}: {str(e)}")

        return result
    except Exception as e:
        logger.error(f"خطای کلی در محاسبه تخفیف: {str(e)}")
        return {
            'total_price': order_price,
            'discount_code': discount_code,
            'discount_id': None,
            'total_discount': 0
        }
