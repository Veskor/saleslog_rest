from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

import accounts.views

urlpatterns = [
    url(_(r'^user/$'),
        accounts.views.UserCreationView.as_view({'get':'list','post':'create'}),
        name='register'),
    url(_(r'^confirm_user'),
        accounts.views.ConfrmUser.as_view({'post':'SetPassword'}),
        name='confirm user'),
]
