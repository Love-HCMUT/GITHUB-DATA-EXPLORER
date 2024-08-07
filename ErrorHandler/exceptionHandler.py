from django.http import JsonResponse

def HandlerException(exception):
    listError = {
        '404' : Error404,
        '500' : Error500, 
        '400' : Error400
    }
    status_code = str(exception.status)
    if (status_code in listError):
        return listError[status_code](exception)
    else:
        return JsonResponse({"message" : "Something went wrong"}, status=status_code)


def Error404(exception): 
    response = {
        "message" : "Wrong infomation", 
        "detail" : str(exception),
    }
    return JsonResponse(response, status=404)


def Error500(exception): 
    response = {
        "message" : "Server has a error", 
        "detail" : str(exception),
    }
    return JsonResponse(response, status=500)


def Error400(exception): 
    response = {
        "message" : "Can not request", 
        "detail" : str(exception),
    }
    return JsonResponse(response, status=400)