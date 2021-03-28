from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from rest_framework.parsers import JSONParser, ParseError
from .serializers import CourierSerializer, OrderSerializer
from .models import Courier, Order
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from dateutil.parser import isoparse
from dateutil.tz import UTC


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
    if request.method == 'GET':
        return see_courier(courier_id)
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
    """
    Creates and saves orders
    """
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


def assign_orders(request):
    """
    Assigning orders so sum of weights of orders is not greater than carrying capacity of courier
    and regions and working hours matching with region and delivery hours
    """
    if request.method == 'POST' and request.body is not None:
        try:
            json = JSONParser().parse(request)
        except ParseError:
            return JsonResponse({'validation_error': 'Impossible to parse to JSON'}, status=400)
        if list(json.keys()) != ['courier_id'] or len(Courier.objects.filter(courier_id=json.get('courier_id'))) != 1:
            return HttpResponseBadRequest('Json should have only courier_id field with existing id of a courier')
        answer, timestamp = validated_assign_couriers(json)
        answer['assign_time'] = timestamp
        return JsonResponse(answer, status=200) if len(answer['orders']) != 0 else JsonResponse({"orders": []})

    return HttpResponseBadRequest('should be POST request with body')


def validated_assign_couriers(json):
    """
    Method to assign orders to couriers using only json that contains order_id
    """
    courier = Courier.objects.filter(courier_id=json.get('courier_id'))[0]
    orders = Order.objects.filter(done=False).filter(region__in=courier.regions).order_by('-weight')
    # We ordering by -weight cause we want to pack from max weight cause in other case foot couriers will not have
    # any light orders all of them will be delivered by high carrying capacity couriers
    suitable_orders = []
    for order in orders:
        if any(CourierSerializer.hours_intersect(delivery_gap, courier.working_hours) for delivery_gap in
               order.delivery_hours):
            suitable_orders.append(order)
    current_payload = sum(order.weight for order in Order.objects.filter(assigned_to=courier).filter(done=False))
    # Here we should pack backpack like in knapsack problem however the dynamic programming method here will not
    # work cause it works only with integer weights so in order not to have exponential
    # time of algorithm(packing by brute force)
    # let's pack it just by Greedy algo
    answer = {
        'orders': [],
        'assign_time': ''
    }
    timestamp = timezone.now().isoformat()
    for order in suitable_orders:
        if courier.courier_type == 'foot' and current_payload + order.weight <= 10 and order.assigned_to is None:
            order.assign_time = timestamp
            order.assigned_to = courier
            order.save()
            answer['orders'].append({'id': order.order_id})
        elif courier.courier_type == 'bike' and current_payload + order.weight <= 15 and order.assigned_to is None:
            order.assign_time = timestamp
            order.assigned_to = courier
            order.save()
            answer['orders'].append({'id': order.order_id})
        elif courier.courier_type == 'car' and current_payload + order.weight <= 50 and order.assigned_to is None:
            order.assign_time = timestamp
            order.assigned_to = courier
            order.save()
            answer['orders'].append({'id': order.order_id})
    return answer, timestamp


def knapsack(space, items):
    """
    Probably we could scale algo to work with float by multiplication by 100 every number. But right now i can't figure
    out how
    """
    w = [item.weight for item in items]
    matrix = [[0 for i in range(space)]] * len(items)

    for k in range(1, len(items)):
        for s in range(1, space):
            if s >= w[k]:
                matrix[k][s] = max(matrix[k - 1][s], matrix[k - 1][s - w[k]] + items[k].weight)
            else:
                matrix[k][s] = matrix[k - 1][s]
    take_orders = []

    def find_orders(k, s):
        if matrix[k][s] == 0:
            return
        print(k - 1, s)
        if matrix[k - 1][s] == matrix[k][s]:
            find_orders(k - 1, s)
        else:
            find_orders(k - 1, s - w[k])
            take_orders.append(items[k])

    find_orders(len(items) - 1, space - 1)


def complete_order(request):
    """
    Mark order as completed
    """
    if request.method == 'POST' and request.body is not None:
        try:
            json = JSONParser().parse(request)
        except ParseError:
            return JsonResponse({'validation_error': 'Impossible to parse to JSON'}, status=400)
        instance = Order.objects.filter(order_id=json.get('order_id'))
        if len(instance) == 0:
            return HttpResponseBadRequest('No such order')
        instance = instance[0]
        courier_instance = Courier.objects.filter(courier_id=json.get('courier_id'))
        if len(courier_instance) == 0:
            return HttpResponseBadRequest('No such courier')
        if instance.assigned_to != courier_instance[0]:
            return HttpResponseBadRequest('Order assigned to different courier')
        if json.get('complete_time') is None:
            return HttpResponseBadRequest('Complete time is needed')
        json['complete_time'] = isoparse(json.get('complete_time')).astimezone(UTC).isoformat()
        serializer = OrderSerializer(instance, data=json, partial=True)
        try:
            serializer.is_valid()
            serializer.save()
            return JsonResponse({"order_id": json.get('order_id')}, status=200)
        except ValidationError as error:
            return HttpResponseBadRequest(error.detail)
    return HttpResponseBadRequest('should be POST request with body')


def see_courier(courier_id):
    if len(Courier.objects.filter(courier_id=courier_id)) == 0:
        return HttpResponseNotFound('Not found')
    courier = Courier.objects.filter(courier_id=courier_id)[0]
    if len(Order.objects.filter(assigned_to=courier).filter(done=True)) == 0:
        answer = {
            "courier_id": courier.courier_id,
            "courier_type": courier.courier_type,
            "regions": courier.regions,
            "working_hours": courier.working_hours,
            "earnings": courier.earnings
        }
        return JsonResponse(answer, status=200)
    time_by_reg = []
    for region in courier.regions:
        orders = Order.objects.filter(region=region).filter(done=True).filter(assigned_to=courier).order_by(
            'complete_time')
        if len(orders) != 0:
            sum_sec = 0
            for i in range(len(orders)):
                if i == 0:
                    sum_sec += (orders[i].complete_time - orders[i].assign_time).total_seconds()
                else:
                    sum_sec += (orders[i].complete_time - orders[i - 1].complete_time).total_seconds()
            time_by_reg.append(sum_sec / len(orders))
    t = min(time_by_reg)
    answer = {
        "courier_id": courier.courier_id,
        "courier_type": courier.courier_type,
        "regions": courier.regions,
        "working_hours": courier.working_hours,
        "rating": round((60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5, 2),
        "earnings": courier.earnings
    }
    return JsonResponse(answer, status=200)
