from django.http import JsonResponse
from rest_framework.parsers import JSONParser, ParseError
from .serializers import CourierSerializer
from rest_framework.exceptions import ValidationError


def upload_couriers(request):
    if request.method == 'POST' and request.body is not None:
        try:
            json = JSONParser().parse(request)
        except ParseError:
            return JsonResponse({'validation_error': {}}, status=400)
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
                error_list['couriers'].append({'id': [courier['courier_id'], error.detail]})
        if valid:
            return JsonResponse(created_list, status=201)
        else:
            return JsonResponse({'validation_error': error_list}, status=400)
    return JsonResponse({'validation_error': {}}, status=400)
