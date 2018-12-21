from core_api.models import *

from accounts.models import User
from django.contrib.auth.models import Group

user = User.objects.create(email='mica@google.com',
                           first_name='Mica',
                           last_name='Ivkovic',
                           username='mica123',
                           gender=User.GENDER_MALE,
                           user_type='super',
                           is_staff=True,
                           is_superuser=True)

#user = User.objects.get(email='mica@google.com')

network = RepairNetwork.objects.create(name='Network')

network.save()

support = Support.objects.create(name='Micin support',
                                 ip='1.1.1.1',
                                 network=network,
                                 fields='',
                                 color='#0693E3')

support.save()

name = support.name + ':' + str(support.id)

group = Group.objects.get(name=name)

group.user_set.add(user)
