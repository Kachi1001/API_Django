from django.http import HttpResponse
def status(request):
    return HttpResponse("Estamos online!!")
