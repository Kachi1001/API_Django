from django.http import HttpResponse
def status(request):
    print (request.headers)
    return HttpResponse("Estamos online!!")
