class DiscountType:
    FIXED = 'fixed'
    PERCENTAGE = 'percentage'

    CHOICES = [
        (FIXED, 'Fixed'),
        (PERCENTAGE, 'Percentage'),
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
