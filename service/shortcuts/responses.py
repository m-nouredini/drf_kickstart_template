from django.http import JsonResponse, HttpResponse


def ok(data=None):
    if not data:
        return HttpResponse(200)
    elif isinstance(data, dict):
        return JsonResponse(data, status=200)
    else:
        return JsonResponse({'message': data}, status=200)


def created(data=None):
    if not data:
        return HttpResponse(201)
    elif isinstance(data, dict):
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({'message': data}, status=201)
