from accounts.models import User
from core_api.models import *

from django.core.management import call_command

group_file = open('accounts/fixtures/group.json', 'w')

call_command('dumpdata',
             'auth',
              stdout=group_file,
             )

models = [
    {
        'file': open('core_api/fixtures/network.json', 'w'),
        'name': 'RepairNetwork',
    },
    {
        'file': open('core_api/fixtures/support.json', 'w'),
        'name': 'Support',
    },
    {
        'file': open('core_api/fixtures/customer.json', 'w'),
        'name': 'Customer',
    },
    {
        'file': open('core_api/fixtures/chain.json', 'w'),
        'name': 'Chain',
    },
    {
        'file': open('core_api/fixtures/ticket.json', 'w'),
        'name': 'Ticket',
    },
    {
        'file': open('core_api/fixtures/message.json', 'w'),
        'name': 'Message',
    },
    {
        'file': open('core_api/fixtures/chat.json', 'w'),
        'name': 'Chat',
    },
    {
        'file': open('core_api/fixtures/repair.json', 'w'),
        'name': 'Repair',
    },
    {
        'file': open('core_api/fixtures/status_type.json', 'w'),
        'name': 'StatusType',
    },
    {
        'file': open('core_api/fixtures/status.json', 'w'),
        'name': 'Status',
    },
    {
        'file': open('core_api/fixtures/engineer.json', 'w'),
        'name': 'Engineer',
    },
    {
        'file': open('core_api/fixtures/equipment.json', 'w'),
        'name': 'Equipment',
    },
    {
        'file': open('core_api/fixtures/part.json', 'w'),
        'name': 'Part',
    },
    {
        'file': open('core_api/fixtures/relation.json', 'w'),
        'name': 'Relation',
    }
]

for item in models:
    call_command('dumpdata',
                 'core_api.{}'.format(item['name']),
                  stdout=item['file'],
                 )

for item in models:
    item['file'].close()
