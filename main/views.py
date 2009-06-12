# Create your views here.

def index(request):
    from django.http import HttpResponse
    return HttpResponse("OK")
