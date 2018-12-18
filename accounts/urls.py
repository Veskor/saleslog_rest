from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

import accounts.views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(_(r'^user/$'),
        accounts.views.UserCreationView.as_view({'get':'list','post':'create'}),
        name='register'),
    url(_(r'^confirm_user/(?P<slug>[-\w]+)$'),
        accounts.views.ConfrmUser.as_view({'post':'SetPassword','get':'CheckSlug'}),
        name='confirm user'),
    url(r'^login/', obtain_jwt_token),
    url(r'^me/', accounts.views.UserMeView.as_view({'get':'get'})),
]
