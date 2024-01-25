
import logging
import requests
from django.http import JsonResponse
from .models import CurrencyRequest
from django.utils import timezone
from django.core.cache import cache
import os
from dotenv import load_dotenv


load_dotenv()

API_KEY=os.getenv('FREE_CURRENCY_API_KEY')


logger = logging.getLogger('currency_app')

def get_current_usd(request):
    logger.debug("Запрос к get_current_usd начат")

   
    last_request_time = cache.get('last_request_time')
    current_time = timezone.now()

    if last_request_time and (current_time - last_request_time).seconds < 10:
        logger.debug("Запрос отклонен, так как прошло менее 10 секунд с последнего запроса")
        return JsonResponse({"error": "Too many requests"})

    response = requests.get(f'https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}&currencies=RUB')
    if response.status_code == 200:
        response_json = response.json()
        rate = response_json['data']['RUB']
        CurrencyRequest.objects.create(timestamp=current_time, usd_to_rub_rate=rate)
        cache.set('last_request_time', current_time, timeout=60) 
        logger.debug(f"Ответ API: {response_json}")
        logger.debug(f"Запись сохранена: {rate}")
    else:
        logger.error(f"Ошибка запроса к API: статус {response.status_code}")

    last_10_requests = CurrencyRequest.objects.order_by('-timestamp')[:10]
    formatted_requests = [{"timestamp": req.timestamp.strftime("%Y-%m-%d %H:%M:%S"), "rate": req.usd_to_rub_rate} for req in last_10_requests]
    
    logger.debug("Запрос к get_current_usd завершен")
    return JsonResponse({"requests": formatted_requests})
