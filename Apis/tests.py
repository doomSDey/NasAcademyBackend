from django.test import TestCase
# Create your tests here.
from rest_framework import status

from Apis.models import Slots


class ApiTest(TestCase):

    def setUp(self):
        Slots.objects.create(slots='1', car='null')
        Slots.objects.create(slots='2', car='null')
        Slots.objects.create(slots='3', car='null')

    # Park a car test cases
    def test_pac(self):
        response = self.client.post('/Apis/park-a-car?car_number=MH10DV3465', )
        self.assertEqual(response.data, {'1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pac_already_parked(self):
        self.client.post('/Apis/park-a-car?car_number=MH10DV3465', )
        response = self.client.post('/Apis/park-a-car?car_number=MH10DV3465', )
        self.assertEqual(response.data, {'Car already parked.'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pac_parking_slot_not_available(self):
        self.client.post('/Apis/park-a-car?car_number=MH10DV3465', )
        self.client.post('/Apis/park-a-car?car_number=MH10DV3466', )
        self.client.post('/Apis/park-a-car?car_number=MH10DV3467', )
        response = self.client.post('/Apis/park-a-car?car_number=MH10DV3468', )
        self.assertEqual(response.data, {'No Parking slot available.Please try after some time'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pac_missing_params(self):
        response = self.client.post('/Apis/park-a-car?', )
        self.assertEqual(response.data, {'Missing parameters'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Unpark a car test cases
    def test_uac(self):
        self.client.post('/Apis/park-a-car?car_number=MH10DV3465', )
        response = self.client.post('/Apis/unpark-a-car?car_number=MH10DV3465', )
        self.assertEqual(response.data, {'Success'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_uac_missing_car(self):
        response = self.client.post('/Apis/unpark-a-car?car_number=MH10DV3465', )
        self.assertEqual(response.data, {'No such car found'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_uac_missing_params(self):
        response = self.client.post('/Apis/unpark-a-car?', )
        self.assertEqual(response.data, {'Missing parameters'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Get car or slot info test cases
    def test_gcosi_car(self):
        self.client.post('/Apis/park-a-car?car_number=MH10DV3465', )
        response = self.client.post('/Apis/get-car-or-slot-info?car_number=MH10DV3465', )
        self.assertEqual(response.data, {'Car number:MH10DV3465,Slot number:1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_gcosi_slots(self):
        self.client.post('/Apis/park-a-car?car_number=MH10DV3465', )
        response = self.client.post('/Apis/get-car-or-slot-info?slots=1', )
        self.assertEqual(response.data, {'Car number:MH10DV3465,Slot number:1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_gcosi_empty_slot(self):
        response = self.client.post('/Apis/get-car-or-slot-info?slots=1', )
        self.assertEqual(response.data, {'Car number:empty,Slot number:1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_gcosi_missing_slot(self):
        response = self.client.post('/Apis/get-car-or-slot-info?slots=MH10DV3465', )
        self.assertEqual(response.data, {'No such slot found'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_gcosi_missing_car(self):
        response = self.client.post('/Apis/get-car-or-slot-info?car_number=MH10DV3465', )
        self.assertEqual(response.data, {'No such car found'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_gcosi_missing_params(self):
        response = self.client.post('/Apis/get-car-or-slot-info?', )
        self.assertEqual(response.data, {'Missing parameters'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
