from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.parsers import JSONParser, ParseError
from .serializers import CourierSerializer, OrderSerializer
from .models import Courier
from rest_framework.exceptions import ValidationError


def upload_couriers(request):
    """
    Creates and saves couriers
    """
    if request.method == 'POST' and request.body is not None:
        try:
            json = JSONParser().parse(request)
        except ParseError:
            return JsonResponse({'validation_error': 'Impossible to parse to JSON'}, status=400)
        valid = True
        error_list = {'couriers': []}
        created_list = {'couriers': []}
        for courier in json['data']:
            serializer = CourierSerializer(data=courier)
            try:
                serializer.is_valid()
                serializer.save()
                created_list['couriers'].append({'id': courier['courier_id']})
            except ValidationError as error:
                valid = False
                error_list['couriers'].append(
                    {'id': ['' if courier.get('courier_id') is None else courier['courier_id'], error.detail]})
        if valid:
            return JsonResponse(created_list, status=201)
        else:
            return JsonResponse({'validation_error': error_list}, status=400)
    return JsonResponse({'request_error': 'should be POST request with body'}, status=400)


def update_couriers(request, courier_id):
    """
    Update info about couriers
    """
    if request.method == 'PATCH' and request.body is not None:
        try:
            json = JSONParser().parse(request)
        except ParseError:
            return JsonResponse({'validation_error': 'Impossible to parse to JSON'}, status=400)
        instance = Courier.objects.filter(courier_id=courier_id)
        if len(instance) == 0:
            return HttpResponseBadRequest('No such courier')
        serializer = CourierSerializer(instance[0], data=json, partial=True)
        try:
            serializer.is_valid()
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        except ValidationError as error:
            return JsonResponse({'validation_error': error.detail}, status=400)
    return HttpResponseBadRequest('Request method should be patch and request should have body')


def upload_orders(request):
    if request.method == 'POST' and request.body is not None:
        try:
            json = JSONParser().parse(request)
        except ParseError:
            return JsonResponse({'validation_error': 'Impossible to parse to JSON'}, status=400)
        valid = True
        error_list = {'orders': []}
        created_list = {'orders': []}
        for order in json['data']:
            serializer = OrderSerializer(data=order)
            try:
                serializer.is_valid()
                serializer.save()
                created_list['orders'].append({'id': order['order_id']})
            except ValidationError as error:
                valid = False
                error_list['orders'].append(
                    {'id': ['' if order.get('order_id') is None else order['order_id'], error.detail]})
        if valid:
            return JsonResponse(created_list, status=201)
        else:
            return JsonResponse({'validation_error': error_list}, status=400)
    return JsonResponse({'request_error': 'should be POST request with body'}, status=400)
