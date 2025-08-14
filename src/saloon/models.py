from django.db import models
from django.conf import settings

# Create your models here.
#* Parent classes
class baseModel(models.Model):
    id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    class Meta:
        abstract = True

class Person(baseModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    CPF = models.CharField(max_length=11, null=False, blank=False, unique=True)          # all digits
    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id} - {self.name}"

#* Registered
class Client(Person):
    phone_number = models.CharField(max_length=16, null=False, blank=False, unique=True)

class Worker(Person):
    active = models.BooleanField(default=True, null=False, blank=False)
    image = models.ImageField(default="placeholder.jpg", null=True, blank=True, upload_to="worker-photos/", editable=True)

class Service(baseModel):
    class serviceType(models.TextChoices):
        HAIR = 'H', 'Hair'
        LASH_STYLING = 'L', 'Lash Styling and Design'

    name = models.CharField(max_length=50, null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=5, null=False, blank=False)
    type = models.CharField(choices=serviceType.choices, default=serviceType.HAIR, null=False, blank=False)

    def __str__(self):
        return f"{self.name} - for R${self.price:.2f}"

#? intermediary tables
class Appointment(baseModel):
    class appointmentStatus(models.TextChoices):
        ONGOING = 'O', 'Ongoing'
        FINISHED = 'F', 'Finished'
        PAID = 'P', 'Paid'
        CANCELLED = 'C', 'Cancelled'

    status = models.CharField(choices=appointmentStatus.choices, default=appointmentStatus.ONGOING, null=False, blank=False)
    date_scheduled = models.DateTimeField(null=False, blank=False)

    #FKs
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    worker = models.ForeignKey(Worker, null=True, on_delete=models.SET_NULL)
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.client.name} at {self.date_scheduled.date()}"

class Payment(baseModel):
    value = models.DecimalField(decimal_places=2, max_digits=5, null=False, blank=False)

    #FKs
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.SET)