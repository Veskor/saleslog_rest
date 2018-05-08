from django.db import models

class RepairNetwork(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Support(models.Model):
    name = models.CharField(max_length=32)
    network = models.ForeignKey(RepairNetwork)

class Customer(models.Model):
    data = models.TextField()

    payment_done = models.BooleanField(default=True)
    #payment = models.ForeignKey(Payment,null=True,blank=True)

    support = models.ForeignKey(Support)

class Chain(models.Model):
    tickets = models.TextField()
    customer = models.ForeignKey(Customer)
#    service_plan = models.ForgeinKey('Payment')

class Part(models.Model):
    name = models.CharField(max_length=32)
    quantity = models.IntegerField()

class Equipment(models.Model):
    name = models.CharField(max_length=32)

class Engineer(models.Model):
    username = models.CharField(max_length=32)

class Status(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Repair(models.Model):
    part = models.ForeignKey(Part) # 1 > ??? Parts.
    equipment = models.ForeignKey(Equipment)
    engineer = models.ForeignKey(Engineer)
    status = models.ForeignKey(Status)

class Ticket(models.Model):
    tag = models.ForeignKey(Chain)
    info = models.TextField()
    repair = models.ForeignKey(Repair)
#    status = models.ForeignKey(Status)

#class Payment(models.Model):
#    service_plan = models.CharField(max_length=32,null=True,blank=True)
#    fixed_price = models.CharField(max_length=32,null=True,blank=True)
#    data = models.TextField()

#    def __str__(self):
#        if not self.service_plan:
#            return self.fixed_price
#        else:
#            return self.service_plan
