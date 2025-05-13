from checkout.models import Order
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import json
import requests
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from core import OrderStatus
from core.logger import logger


@method_decorator(login_required, name='dispatch')
class ToBank(View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id, user_id=request.user.id, status=OrderStatus.PENDING_PAYMENT)
        logger.info(f"Starting payment process - Order: {order.id} - User: {request.user.username}")

        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": order.total_price,
            "description": f'sandbox, order: {order.id}',
            "callback_url": settings.ZARINPAL_CALLBACK_URL,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        try:
            response = requests.post(settings.ZARINPAL_REQUEST, data=data, headers=headers, timeout=10)
        except requests.exceptions.Timeout:
            logger.error(f"Timeout error in payment - Order: {order.id}")
            order.status = OrderStatus.FAILED
            order.save()
            return render(request, 'to_bank.html', {'error': 'time out error'})
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error in payment - Order: {order.id}")
            order.status = OrderStatus.FAILED
            order.save()
            return render(request, 'to_bank.html', {'error': 'connection error'})

        if response.status_code != 200:
            logger.error(f"Status code error in payment - Order: {order.id} - Code: {response.status_code}")
            order.status = OrderStatus.FAILED
            order.save()
            return render(request, 'to_bank.html', {'error': f'response status code: {response.status_code}'})

        response = response.json()
        if response['data']['code'] != 100:
            logger.error(f"Zarinpal status code error - Order: {order.id} - Code: {response['data']['code']}")
            order.status = OrderStatus.FAILED
            order.save()
            return render(request, 'to_bank.html', {'error': f'status error code: {response["data"]["code"]}'})

        authority = response['data']['authority']
        order.zarinpal_authority = authority
        order.status = OrderStatus.PENDING_PAYMENT
        order.save()
        logger.info(f"Redirecting to payment gateway - Order: {order.id} - User: {request.user.username}")
        return redirect(settings.ZARINPAL_STARTPAY + authority)


class Verify(View):
    def get(self, request, *args, **kwargs):
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')

        order = get_object_or_404(Order, zarinpal_authority=authority)
        logger.info(f"Payment verification - Order: {order.id} - Status: {status}")

        if not status or status != 'OK':
            logger.warning(f"Unsuccessful payment - Order: {order.id}")
            order.status = OrderStatus.FAILED
            order.save()
            return render(request, 'verify.html')

        data = {
            "merchant_id": settings.ZARINPAL_MERCHANT_ID,
            "amount": order.total_price,
            "authority": order.zarinpal_authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        try:
            response = requests.post(settings.ZARINPAL_VERIFY, data=data, headers=headers, timeout=10)
        except requests.exceptions.Timeout:
            logger.error(f"Timeout error in payment verification - Order: {order.id}")
            order.status = OrderStatus.FAILED
            order.save()
            return render(request, 'verify.html', {'error': 'time out error'})
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error in payment verification - Order: {order.id}")
            order.status = OrderStatus.FAILED
            order.save()
            return render(request, 'verify.html', {'error': 'connection error'})

        if response.status_code != 200:
            logger.error(f"Status code error in payment verification - Order: {order.id} - Code: {response.status_code}")
            order.status = OrderStatus.FAILED
            order.save()
            return render(request, 'verify.html', {'error': f'response status code: {response.status_code}'})

        response = response.json()
        if response['data']['code'] != 100:
            logger.error(f"Zarinpal status code error in verification - Order: {order.id} - Code: {response['data']['code']}")
            order.status = OrderStatus.FAILED
            order.save()
            return render(request, 'verify.html', {'error': f'status error code: {response["data"]["code"]}'})

        ref_id = response['data']['ref_id']
        order.zarinpal_ref_id = ref_id
        order.status = OrderStatus.PROCESSING
        order.save()
        logger.info(f"Successful payment - Order: {order.id} - Tracking code: {ref_id}")
        return render(request, 'verify.html', {'ref_id': ref_id})
