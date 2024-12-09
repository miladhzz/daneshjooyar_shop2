from .models import SpecialPrice


def get_min_special_price(product):
    from shop.models import Category
    specialPrices = SpecialPrice.objects.active().all()
    # باید همه رو بیارم نمیشه بگم بالاترین شون.
    pp = []
    for specialPrice in specialPrices:
        products = specialPrice.products.filter(id=product.id)
        if products.exists():
            pp.append(
                {
                    'id': specialPrice.id,
                    'fixed': specialPrice.fixed,
                }
            )

    max_special = max(pp, key=lambda x: x['fixed'])
    m = 0
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


    return None
