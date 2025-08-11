# ORM querys for usage in renderers

from decimal import Decimal
import inspect
from datetime import date, datetime, timedelta

from django.db.models import Model
from django.conf import settings
from django.db.models import Count, Q

from saloon import models

MODEL_CHOICES: dict[str, Model] = { 
    name.lower(): obj 
    for name, obj in inspect.getmembers(models, inspect.isclass)
    if issubclass(obj, Model) and not (obj is Model) and not getattr(obj._meta, "abstract", False)
}
if settings.DEBUG: print(MODEL_CHOICES)

#* All data
def load_data_range(modelOption: str, range: int = 15, offset: int = 0) -> list[Model]: 
    """Load a range of registrys from a model

    Args:
        modelOption (str): chooses from MODEL_CHOICES (all concrete, registered models from models.py)
        range (int, optional): Defaults to 15. If 0, will get all registrys
        offset (int, optional): Defaults to 0.

    Raises:
        KeyError: if modelOption is not valid
    """
    model: Model = MODEL_CHOICES.get(modelOption.lower(), None)

    if not model: raise KeyError(f"The modelOption '{modelOption}' inserted does not exist.")

    #special conditions
    match(modelOption):
        case "worker":
            #load with data about related appointments
            return model.objects.annotate(
                ongoing_schedules=Count('appointment', filter=Q(appointment__status='ONGOING')),
                finished_schedules=Count('appointment', filter=Q(appointment__status='FINISHED'))
            )
        case _:
            pass

    if range == 0:
        results = model.objects.all()
    else:
        limit: int = range + offset
        results = model.objects.all()[offset:limit]

    return results

#* Relational data per demand
def load_all_appointments_today() -> list[models.Appointment]:
    today = datetime.now()
    end = today + timedelta(hours=23, minutes=59, seconds=59)
    return models.Appointment.objects.filter(
        date_scheduled__gte=today,
        date_scheduled__lt=end,
    ).all()

def load_ongoing_appointments_next_hour() -> int:
    start = datetime.now()
    end = start + timedelta(hours=1)
    return models.Appointment.objects.filter(
        date_scheduled__gte=start,
        date_scheduled__lt=end,
        status=models.Appointment.appointmentStatus.ONGOING
    ).all().count()

def load_finished_appointments_today() -> int:
    today = datetime.now()
    end = today + timedelta(hours=23, minutes=59, seconds=59)
    return models.Appointment.objects.filter(
        date_scheduled__gte=today,
        date_scheduled__lt=end,
        status=models.Appointment.appointmentStatus.FINISHED
    ).all().count()

def load_value_revenue_today() -> Decimal:
    today = datetime.now()
    end = today + timedelta(hours=23, minutes=59, seconds=59)
    resultsFinished = models.Appointment.objects.filter(
        date_scheduled__gte=today,
        date_scheduled__lt=end,
        status=models.Appointment.appointmentStatus.FINISHED
    ).all()

    totalRevenue: Decimal = 0.00
    for appointment in resultsFinished:
        if appointment.service:
            totalRevenue += appointment.service.value
    
    return totalRevenue