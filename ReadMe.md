
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
  
# Solution overview  
  
During the initialization of the server a sqlite db is initalized that pulls the lot size from the .env file and then initialized that many rows with lot number ranging from 1 to the lot size + 1 while the car value is initialized to 'null'.  
  
 - **Park a Car:** Checks for car name duplicacy and then it check for a avaiable slot ( any slot with 'null' value) and assigns it the slot and returns the slot value.  
 - **Unpark the Car:** Checks if the car is actually present and if so assigns 'null' to the car value and returns 'Success'  
 - **Get the Car/Slot Information:** Check if the slot or car is actually avaiable and if so then returns both the car and the slot value.  
 - **Rate Limiting Algo:** Extracts the ip and keeps a time and count which resets if there are less than 10 request per ip in 10 sec and sends a timeout message otherwise. This algo will break under concurrent requests.  
  
**Note:** All the API check for missing/invalid params and also has a common rate limiting algo that's called.  
I could have used a persistent datastructure instead of sqlite db but that I think would be a poor design and since sqlite is a integral part of Django and doesn't need any external imports hence I used it.  
  
**Database structure overview:**  
  
 - **Slots:** Contains two fields 'slots' and 'car' which is used to keep track of the cars and slots transactions that the API actually executes. *Primary key: slots*  
 - **RateCount:** Contains 3 fields 'ip', 'count' and 'date_time'. This is used by the rate limiting function. *Primary key: ip*  
  
[**FlowDiagram**](https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=1.drawio#R5V1tc5s4EP41nn6yBwmJl49J2vRupr3JNL259qNqFJsLBh/gJr5ff8IgbL3E5sZGojgfEiPzus9q99ldLZm4d6vXjzlZLz9nEU0m0IleJ%2b77CWQ/IGB/qpFtPRIEXj2wyOOoHgL7gcf4X9oMOs3oJo5oIexYZllSxmtxcJ6lKZ2XwhjJ8%2bxF3O0pS8SrrsmCKgOPc5Koo3/FUblsngL6%2b/HfaLxY8isDL6y/WRG%2bc/MkxZJE2cvBkPth4t7lWVbWn1avdzSphMflUh93/8a37Y3lNC27HLDx7qdfb/B2/n3uRc78G7j//H7q1mf5SZJN88DNzZZbLoE826QRrU7iTNzbl2Vc0sc1mVffvjDM2diyXCVsC7CPzeloXtLXN%2b8TtE/P1IZmK1rmW7ZLc4AbNPewFTXhZS9%2brxlaHkjebcZIA/iiPfFeJuxDI5b/ISKET8uIRkxpms0sL5fZIktJ8mE/eitKcb/PpyxbN7L7m5bltpkBZFNmOslWFzouV3Zf2Saf02NP1Mwjki9oeWQ/gPRA5TQhZfxTvJHLy10R%2b83D74UieqZopSiposyzZ3qXJVnORtIsreT/FCeJNESSeJGyzTkTIGXjt5Xaxmzq3zRfrOIo2oGnU3oR0EvofSjpPVb0Hmn0Hval94DfgFk9Z9LKt9%2bq42eYb35vTrfbeP8qbG0FBC4yP/yu88MJbE4Qf3i2G2NRh3VK7AeqEqO%2blDhQZPSRQcpklDC3C%2b/nJK/OkD5l47UrGPsiJtCfqah4GlQ4eBdHJRye5sqso7WrtmgHcLxB8I4B2GPOAE8a5NDRY2zGHvPbPADsz5Q973N1sSpEqYzNWK2MzF6Y3bFLX9yrnS08TD41W95CtPNsaQ59yOK0PPA3jqgIWEK4vq/mIAnk9i7Ooa3Dcy6yb7Ed0gKoyOhhb6fuxmynZDNlO8pC/rWaqc5ZCGjTqaPANj4%2bEhCaOa57AqXd1gPNYyaCaspZg863iRwGdpETUcMDnFkotImPN4z45uKCvzihQtxdy6GpKUalZmJVRrXMVj82hZlQ3RflATR0KtD48KA3OqVWCD7HRRGnCzbIiBVZXVPaGqlomM1bqzk/VV0tZ5c82wGAmoH7QkrKRj7Fq7hSq6vRV892ngLZpSnWAgDYOU/h9uJWp1KiwvXNulX3Wstr3YH3zgT%2brInJTzwU2gOkvJrGhxhlPVwcB/KJnyZNmtshSU5JVN3%2bOqcFbabQOD2KZEectwnQ5UEY4AKeKZAlEqoSAdgk34FqCPOFlps8ZWPv7mSFJfkzjd6NV2GnAMoAqSSoBdEMC/JsO0MfHLrDqTNzAstpNuh19JPuuWVPPUFqrVajJSg0S5D45a3phOd4sk6AX0UnoNXcHuyQ2zPJncJAtHeaHIVZ7qSu3SK7o6p1SQX7%2b7SpNsfqgACQ8PAt54zgAHNGUylRgTW8sg0KzLAoTdaoZVF/ZJNdsvO5TnvWC%2bwc8pPECfmR0NlDQklRZZjqhyRPuywTs3ir3SAzmGNmXCGQsFQJF3Q0S/D6I1zqYiXrGg8wPqnxZuMGV80BtBr/WGt4uln9GHO%2bFHgyKLZjBaSC8jVnn0YLwVSOp22XWJCa%2bhk3AsAXCQtybSOg5n3uSVKMGAI8NATUlNLIEZCCKGibtKMBthFgKWeCLfe/YJXmtQRmAr1/NlX36a26WoF/M15txkjkNZ71rhjeO3U9FkVuFwO2TQq%2bOreKoDgNQGAbgqvzqwCIDXr2Z4G6nm3c9B5JdkhTDjMKQGB90fnEztIQXmE63ekH9YCeW/KSCwWB5Ox7LnkFoWXgEXYnYskLoBPw913y6q4T55a89DqB%2bBtruE5gszoRqhReURKjy6%2bxHAeq1tJoMS1U84EHC5HGv/xIyk25upY22Jfs1ZhFVU7DMTiUqotIl7E2WkYI1bBiXzh73MzntChGXP2CUAJE07BhtoQQDrDe6/KOdS4lTe7IbL03PFnvLTbzZWtpnyqBjViNFYA0K3DNFnGBo5rfcUdqrrxyRDNJzHYbOWqwPPJ8hdyP6GoIoOE3lY2vlZTbkdPt8eDc13icKXsrIaslUZ/b0K6PMD3uSPiEgs7MOfiRyPsb8eZNnpPtwW7raofi2FWBdFVX0ob6jBcNZlthDyWaxViUAtTkv802Ezsq69qHs/fNurrRR7XYd0Xt5O/1MdFVAzSv8lK11HB8ICepoaarhnfGH2qq15%2bUjqyOU%2bMDrrpjDxOQ/L7FUFtZ1iCF%2bqosA80Ln6zrs/xeShTYjncBOJKnqbvE%2bGrP6uKMf6zW5c7lphH7/ekq1oMqsGnMkOEoGHbQ7uuon7Wl5A5cFuphPpvLinwKyUSp75fVdGk9%2bsUClO6g1os57MWCXV5JbZDce443E5e3uAhqnHHLuYV1Xk5/7lgNgnYUv2FIZbaDrHE8y52raV8g6%2bz2d96lmyQZMYvykBSddlyTgXpzMmpIMO5Uq%2bdKkbGWx5pN9GneyTHyZCvmGn0k6jOMQZfXwRmOJXy5Q0aTxTEcS0C1LvBmLHFF4YOKlO1OSKBpxh65Zfcljm69iKbpvx65XfcdaR70hwHb3P%2bXsTrO2v%2bvNvfDfw==)