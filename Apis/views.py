from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import time

# Create your views here.
from Apis.models import RateCount, Slots


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
            return "exceed"
        return "ok"
    except Exception as e:
        print(e)
        print("Ip not in db")
        r = RateCount(ip=ip, count=1, date_time=time.time())
        r.save()
        client = RateCount.objects.get(ip=ip)
        print(client.ip)
        return "ok"


# Apis

@api_view(['POST'])
def park_a_car(request):
    if rate_limiter(request) == "exceed":
        return Response({'Number of request exceeded.Please try again after some time'})

    if 'car_number' not in request.GET:
        return Response({'Missing parameters'})

    car_number = request.GET['car_number']

    if (Slots.objects.filter(car = car_number)).exists():
        return Response({'Car already parked.'})

    s = Slots.objects.filter(car = 'null').first()

    if s is None:
        return Response({'No Parking slot available.Please try after some time'})
    else:
        s.car = car_number
        s.save()

    print(s.slots)
    return Response({s.slots})

@api_view(['POST'])
def unpark_a_car(request):
    if rate_limiter(request) == "exceed":
        return Response({'Number of request exceeded.Please try again after some time'})

    if 'car_number' not in request.GET:
        return Response({'Missing parameters'})

    s = Slots.objects.filter(car = request.GET['car_number']).first()

    if s is None:
        return Response({'No such car found'})
    else:
        s.car = 'null'
        s.save()
    return Response({'Success'})

@api_view(['POST'])
def get_car_or_slot_info(request):
    if rate_limiter(request) == "exceed":
        return Response({'Number of request exceeded.Please try again after some time'})

    if 'slots' in request.GET:
        s = Slots.objects.filter(slots = request.GET['slots']).first()
        if s is None:
            return Response({'No such slot found'})
        else:
            if s.car == 'null':
                return Response({'Car number:'+'empty'+',Slot number:'+s.slots})
            else:
                return Response({'Car number:'+s.car+',Slot number:'+s.slots})
    elif 'car_number' in request.GET:
        s = Slots.objects.filter(car = request.GET['car_number']).first()
        if s is None:
            return Response({'No such car found'})
        else:
            return Response({'Car number:'+s.car+',Slot number:'+s.slots})
    else:
        return Response({'Missing parameters'})

@api_view(['POST'])
def show_table(request):
    s = Slots.objects.all()
    for i in s:
        print(i.slots,' ',i.car)
    return Response({'Success'})
