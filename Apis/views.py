from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import time

# Create your views here.
from Apis.models import RateCount


def index(request):
    return HttpResponse("Hello, world.")


def rate_limiter(request):
    ip: str
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print("ip", ip)
    try:
        client = RateCount.objects.get(ip=ip)
        print("ip qy=uery", client.ip, client.count)
        if ((time.time() - float(client.date_time)) % 60) > 10:
            RateCount.objects.filter(ip=ip).update(count=1, date_time=time.time())
        else:
            RateCount.objects.filter(ip=ip).update(count=client.count + 1)
        if client.count >= 10 and ((time.time() - float(client.date_time)) % 60) <= 10:
            return Response({'Number of request exceeded.Please try again after some time'})
        return Response({'ok'})
    except Exception as e:
        print(e)
        print("Ip not in db")
        r = RateCount(ip=ip, count=1, date_time=time.time())
        r.save()
        client = RateCount.objects.get(ip=ip)
        print(client.ip)
        return Response({'ok'})


# Apis

@api_view(['POST'])
def park_a_car(request):
    return rate_limiter(request)
