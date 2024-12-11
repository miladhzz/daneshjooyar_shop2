from .models import SpecialPrice
from django.db.models import Q


def get_max_special_price(product):
    active_special_prices = SpecialPrice.objects.active().filter(
        Q(products=product) | Q(categories=product.category)
    ).distinct()

    # active_special_prices = SpecialPrice.objects.active().all()
    # شاید ک قبلی با دسته بندی مچ نبود

    max_special = {
        'fixed_type': None,
        'fixed': None,
        'percent_type': None,
        'percent': None,
    }

    for special_price in active_special_prices:
        # if special_price.products.filter(id=product.id).exists():
        # شاید وقتی از دسته بندی استفاده کنم لازم باشه

        if max_special['fixed'] is None or special_price.fixed > max_special['fixed']:
            max_special['fixed_type'] = special_price.type
            max_special['fixed'] = special_price.fixed

        if max_special['percent'] is None or special_price.percent > max_special['percent']:
            max_special['percent_type'] = special_price.type
            max_special['percent'] = special_price.percent

    return max_special



