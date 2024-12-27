class DiscountType:
    FIXED = 'fixed'
    PERCENT = 'percent'

    CHOICES = [
        (FIXED, 'Fixed'),
        (PERCENT, 'Percent')
    ]


class OrderStatus:
    PENDING_PAYMENT = 'pending_payment'
    FAILED = 'failed'
    CANCELED = 'canceled'
    PROCESSING = 'processing'
    COMPLETED = 'completed'

    CHOICES = [
        (PENDING_PAYMENT, 'pending_payment'),
        (FAILED, 'failed'),
        (CANCELED, 'canceled'),
        (PROCESSING, 'processing'),
        (COMPLETED, 'completed'),
    ]
