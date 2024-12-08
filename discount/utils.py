from .models import DiscountPrice


def get():
    from shop.models import Category

    m = DiscountPrice.objects.filter(status=True)

    m = DiscountPrice.objects.all()[0]
    m2 = m.categories.all()

    m = Category.objects.first()
    n = m.discountprice_set.all()

    n = DiscountPrice.categories.through.objects.all()

    n = DiscountPrice.objects.filter(categories__id=1)

    n = DiscountPrice.categories.through.objects.filter(discountprice__status=True)


    return None
