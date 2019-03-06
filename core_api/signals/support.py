from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json

from ..models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=Support, dispatch_uid='create_support_role')
def create_role(sender, instance, **kwargs):
    # Tickets
    ticket_ct = ContentType.objects.get(model='ticket')
    name = instance.name + ':' + str(instance.id)

    can_edit_tickets, created = Permission.objects.get_or_create(name='Can Edit {}'.format(name), codename='can_edit_tickets_{}'.format(name),
                       content_type=ticket_ct)

    if created == True:
        can_edit_tickets.save()
    else:
        can_edit_tickets = None

    can_view_tickets, created = Permission.objects.get_or_create(name='Can View {}'.format(name), codename='can_view_tickets_{}'.format(name),
                       content_type=ticket_ct)
    if created == True:
        can_view_tickets.save()
    else:
        can_view_tickets = None

    # Customers
    customer_ct = ContentType.objects.get(model='customer')

    can_edit_customers, created = Permission.objects.get_or_create(name='Can Edit {}'.format(name), codename='can_edit_customers_{}'.format(name),
                       content_type=customer_ct)
    if created == True:
        can_edit_customers.save()
    else:
        can_edit_customers = None

    can_view_customers, created = Permission.objects.get_or_create(name='Can View {}'.format(name), codename='can_view_customers_{}'.format(name),
                       content_type=customer_ct)
    if created == True:
        can_edit_customers.save()

    group, created = Group.objects.get_or_create(name=name)

    if created == True:
        group.save()
        group.permissions.add(can_edit_tickets)
        group.permissions.add(can_view_tickets)
        group.permissions.add(can_edit_customers)
        group.permissions.add(can_view_customers)

    relation = Relation.objects.create(model='Support',model_id=instance.id)

    relation.save()

    status_type = StatusType.objects.create(relation=relation)

    status_type.save()
