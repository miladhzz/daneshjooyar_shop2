from .models import SpecialPrice


def get_max_product_fix_special_price(product):
    active_special_prices = SpecialPrice.objects.active().all()
    # باید همه رو بیارم نمیشه بگم بالاترین شون.
    max_special = {
        'fixed_type': None,
        'fixed': None,
        'percent_type': None,
        'percent': None,
    }

    for special_price in active_special_prices:
        if special_price.products.filter(id=product.id).exists():

            if max_special['fixed'] is None or special_price.fixed > max_special['fixed']:
                max_special['fixed_type'] = special_price.type
                max_special['fixed'] = special_price.fixed

            if max_special['percent'] is None or special_price.percent > max_special['percent']:
                max_special['percent_type'] = special_price.type
                max_special['percent'] = special_price.percent

    return max_special
    # m = DiscountPrice.objects.filter(status=True)
    #
    # m = DiscountPrice.objects.all()[0]
    # m2 = m.categories.all()
    #
    # m = Category.objects.first()
    # n = m.discountprice_set.all()
    #
    # n = DiscountPrice.categories.through.objects.all()
    #
    # n = DiscountPrice.objects.filter(categories__id=1)
    #
    # n = DiscountPrice.categories.through.objects.filter(discountprice__status=True)


