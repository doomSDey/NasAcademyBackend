from django.test import TestCase, client


# Create your tests here.
from django.urls import reverse
from rest_framework import status

from Apis.models import Slots


class ApiTest(TestCase):

    def setUp(self):
        Slots.objects.create(slots = '1',car = 'null')
        Slots.objects.create(slots = '2',car = 'null')
        Slots.objects.create(slots = '3',car = 'null')

    # Park a car test cases
    def test_pac(self):
        response = self.client.post('/Apis/park-a-car?car_number=MH10DV3465',)
        self.assertEqual(response.data,{'1'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_pac_already_parked(self):
        self.client.post('/Apis/park-a-car?car_number=MH10DV3465',)
        response = self.client.post('/Apis/park-a-car?car_number=MH10DV3465',)
        print('res',response.data)
        self.assertEqual(response.data,{'Car already parked.'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_pac_parking_slot_not_available(self):
        self.client.post('/Apis/park-a-car?car_number=MH10DV3465',)
        self.client.post('/Apis/park-a-car?car_number=MH10DV3466',)
        self.client.post('/Apis/park-a-car?car_number=MH10DV3467',)
        response = self.client.post('/Apis/park-a-car?car_number=MH10DV3468',)
        self.assertEqual(response.data,{'No Parking slot available.Please try after some time'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_pac_missing_params(self):
        response = self.client.post('/Apis/park-a-car?',)
        print('res',response.data)
        self.assertEqual(response.data,{'Missing parameters'})
        self.assertEqual(response.status_code,status.HTTP_200_OK)