from .models import SpecialPrice
from core import DiscountType
from django.db.models import Q


def get_special_price(product):
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
