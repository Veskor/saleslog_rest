from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views.support import SupportViewset
from .views.repair import RepairNetworkViewset, RepairViewset
from .views.customer import CustomerViewset, upload_file
from .views.chain import ChainViewset, StatusViewSet, ChatsViewSet, MessageViewSet
from .views.ticket import TicketViewset

router = DefaultRouter()

router.register(r'network', RepairNetworkViewset)
router.register(r'network/(?P<id>\d+)/repair', RepairViewset)
router.register(r'customer', CustomerViewset)
router.register(r'chain', ChainViewset)
router.register(r'ticket', TicketViewset)
router.register(r'chat', ChatsViewSet)
router.register(r'tags', StatusViewSet)
router.register(r'message', MessageViewSet)
router.register(r'support', SupportViewset)

urlpatterns = [
    url(r'upload/', upload_file),
    url(r'accounts/', include('accounts.urls')),
    url(
            r'',
                include(
                            router.urls,
                        ),
            ),
        ]
