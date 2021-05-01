import sys

from django.apps import AppConfig
import os
from dotenv import load_dotenv


load_dotenv()


class ApisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Apis'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        lot_size = os.getenv('lot_size')
        from Apis.models import Slots
        Slots.objects.all().delete()
        for i in range(0,int(lot_size)):
            s = Slots(slots = i,car = 'null')
            s.save()