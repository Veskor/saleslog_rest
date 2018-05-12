from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Chain)
admin.site.register(Customer)
admin.site.register(Part)
admin.site.register(Equipment)
admin.site.register(Engineer)
admin.site.register(Status)
admin.site.register(Repair)
admin.site.register(Ticket)
