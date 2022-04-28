from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime

# Create your models here.

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = PhoneNumberField()
    address = models.CharField(max_length=250)
    citizenship_id = models.BigIntegerField(null=False, blank = False, default = 0)
    pan_no = models.IntegerField(null = False, blank=False,default=0)
    avatar = models.ImageField(default = "default.png", upload_to = "profile_picture/")
    citizenship = models.FileField(default = "citizen_default.jpg", upload_to = "citizenship/")

    def __str__(self):
        return f"{self.user.username} profile"

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Parking(models.Model):
    parking_id = models.AutoField(primary_key=True)
    slot_number = models.IntegerField()
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.slot_number}-->{self.occupied}"

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    slot_allotted = models.IntegerField(null=True, blank=True)
    ticket_issued = models.DateTimeField(auto_now_add = True)
    created = models.DateTimeField(auto_now_add = True)
    active = models.BooleanField(default=True)

    def save(self,*args,**kwargs):
        queryset = Parking.objects.filter(occupied = False).order_by('slot_number')
        slot = queryset.first().slot_number
        if queryset.exists():
            self.slot_allotted = slot
        else:
            self.slot_allotted = 0
            self.active  = False
        super(Ticket, self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.slot_allotted}"

class Car(models.Model):
    STATUS = (
        ('Parked','Parked'),
        ('Departed','Departed'),
    )

    car_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket,related_name = 'ticket',on_delete=models.DO_NOTHING)
    colour = models.CharField(max_length = 25)
    numberplate = models.CharField(max_length=50)
    model = models.CharField(max_length=50) 
    status = models.CharField(max_length = 25,choices=STATUS, default="Parked")

    def __str__(self):
        return f"{self.model}-{self.numberplate}"

class Bill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    exit_time = models.DateTimeField(auto_now_add = True)
    total_bill = models.IntegerField(default = 10)

    def save(self,*args,**kwargs):
        parked_time = self.ticket.created.time().hour
        now = datetime.now().time().hour
        total_time = now - parked_time
        if abs(total_time) <= 1:
            self.total_bill = 10
        elif abs(total_time) > 24:
            self.total_bill = 240 + (total_time * 10)
        else:
            self.total_bill = total_time * 10
        super(Bill, self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.ticket}-->{self.total_bill}"

class Payment(models.Model):
    BILL_STATUS = (
        ('Paid','Paid'),
        ('Unpaid','Unpayed'),
    )   

    payment_id = models.AutoField(primary_key = True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    total_payment = models.FloatField()
    status = models.CharField(max_length=25, choices=BILL_STATUS,default='Unpaid')
    payment_date = models.DateTimeField(auto_now_add = True)
    




    

    
    
    

