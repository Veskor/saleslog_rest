from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json

from ..models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=Support, dispatch_uid='create_support_role')
def create_role(sender, instance, **kwargs):
    return
    # Tickets
    ticket_ct = ContentType.objects.get(model='ticket')


    can_edit_tickets = Permission(name='Can Edit', codename='can_edit_tickets',
                       content_type=ticket_ct)

    can_view_tickets = Permission(name='Can View', codename='can_view_tickets',
                       content_type=ticket_ct)

    can_edit_tickets.save()
    can_view_tickets.save()


    # Customers
    customer_ct = ContentType.objects.get(model='customer')

    can_edit_tickets = Permission.objects.create(name='Can Edit', codename='can_edit_customers',
                       content_type=customer_ct)

    can_view_tickets = Permission.objects.create(name='Can View', codename='can_view_customers',
                       content_type=customer_ct)

    can_edit_tickets.save()
    can_view_tickets.save()

    created = Group.objects.create(name=instance.name)

    created.save()

    created.permissions = [can_edit_tickets,can_view_tickets,can_edit_customers,can_view_customers]
