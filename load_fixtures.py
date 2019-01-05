import os
from django.core.management import call_command

models = os.listdir('core_api/fixtures')

error_log = {
            'failed': 0,
            'errors': [],
            }

for item in models:
    try:
        call_command('loaddata', 'core_api/fixtures/' + item)
    except as e:
        error_log['failed'] += 1
        error_log['errors'].append(e)

if error_log['failed'] > 0:
    print('FAILED :' + str(error_log['failed']))
    for item in error_log['errors']:
        print(item)
