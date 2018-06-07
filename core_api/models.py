from django.db import models

class RepairNetwork(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Support(models.Model):
    name = models.CharField(max_length=32)
    network = models.ForeignKey(RepairNetwork)
    fields = models.TextField(default='')

    def __str__(self):
        return self.name

class Customer(models.Model):
    data = models.TextField()

    payment_done = models.BooleanField(default=True)
    #payment = models.ForeignKey(Payment,null=True,blank=True)

class Chain(models.Model):
    tickets = models.TextField(null=True)
    customer = models.ForeignKey(Customer)
    statuses = models.TextField(null=True)
    chats = models.TextField(null=True)
#    service_plan = models.ForgeinKey('Payment')

    def __str__(self):
        return self.customer.data

class Part(models.Model):
    name = models.CharField(max_length=32)
    quantity = models.IntegerField()
    network = models.ForeignKey(RepairNetwork,default='')

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=32)
    network = models.ForeignKey(RepairNetwork,default='')

    def __str__(self):
        return self.name

class Engineer(models.Model):
    username = models.CharField(max_length=32)
    network = models.ForeignKey(RepairNetwork,default='')

    def __str__(self):
        return self.username

class Status(models.Model):
    name = models.CharField(max_length=32)
    color = models.CharField(max_length=6,default='')
    chain = models.ForeignKey(Chain,default='')

    def __str__(self):
        return self.name

class Repair(models.Model):
    part = models.ForeignKey(Part) # 1 > ??? Parts.
    equipment = models.ForeignKey(Equipment)
    engineer = models.ForeignKey(Engineer)

    def __str__(self):
        return self.status

class Chat(models.Model):
    TICKET = 'Ticket'
    MASTER = 'Master'
    TYPE_CHOICES = (
        (TICKET, 'Ticket'),
        (MASTER, 'Master')
    )
    origin = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TICKET)
    tag = models.ForeignKey(Chain,default='')

class Message(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=32)
    chat = models.ForeignKey(Chat,default='')

class Ticket(models.Model):
    tag = models.ForeignKey(Chain)
    info = models.TextField()
    repair = models.ForeignKey(Repair,blank=True,null=True)
    support = models.ForeignKey(Support,default='')
    status = models.ForeignKey(Status,blank=True,null=True)
    chat = models.ForeignKey(Chat,blank=True,null=True)


#class Payment(models.Model):
#    service_plan = models.CharField(max_length=32,null=True,blank=True)
#    fixed_price = models.CharField(max_length=32,null=True,blank=True)
#    data = models.TextField()

#    def __str__(self):
#        if not self.service_plan:
#            return self.fixed_price
#        else:
#            return self.service_plan
