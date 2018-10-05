from django.conf import settings

#from .customer import *    # ---
#from .repair import *      # ---
#from .ticket import *      # ---
#from .support import *     # ---
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saleslog_rest.settings")
django.setup()


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

from .test_chain import *       # ....
from .test_customer import *
