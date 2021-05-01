# Objective:
### Create three API endpoints:

 - **Park a Car:** The Endpoint will be given the car number as input and outputs the slot where it is parked. 
 - **Unpark the Car:** This endpoint takes the slot number from which the car is to be removed from and frees that slot up to be used by other cars.
 - **Get the Car/Slot Information:** This endpoint can take either the slot number or car number and return both the car number and slot number for the input.

**Note:** The server will rate-limit the number of requests coming in. So, if a user makes more than 10 requests in 10 seconds, we return the appropriate error message.

# Getting the App up and running:
Run the following commands to get the server up and running:
 - `python manage.py makemigrations Apis`
 - `python manage.py migrate`
 - `python manage.py runserver 0.0.0.0:8000` (launches the server on localhost with port number 8000)
 
Change "lot_size" value in .env to modify the parking lot size. The lot size is reintiallized each time "runserver" command is executed.

# Running Unit Tests
A series of unit tests for each module has been written which can be executed by the command:

    python manage.py test

# Hitting the API using Postman
One can directly put the following urls and set the method as "POST" and use Postman or any other testing app like Jmeter etc to test the APIs.

Modify "MH10DV3465" to any car number you want
 - for parking car:
	 - http://0.0.0.0:8000/Apis/park-a-car?car_number=MH10DV3465
- for unparking car:
	- http://0.0.0.0:8000/Apis/unpark-a-car?car_number=MH10DV3465
- for getting info on slot/car number (change "car_number" to "slots" for querying with slots:
	- http://0.0.0.0:8000/Apis/get-car-or-slot-info?car_number=MH10DV3465 
