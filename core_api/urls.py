from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views.support import SupportViewset
from .views.repair import RepairNetworkViewset
from .views.customer import CustomerViewset
from .views.chain import ChainViewset, StatusViewSet, ChatsViewSet, MessageViewSet
from .views.ticket import TicketViewset

router = DefaultRouter()
network_detail = RepairNetworkViewset.as_view({'get': 'retrieve'})
router.register(r'support', SupportViewset)
router.register(r'network', RepairNetworkViewset)
router.register(r'customer', CustomerViewset)
router.register(r'chain', ChainViewset)
router.register(r'ticket', TicketViewset)
router.register(r'chat', ChatsViewSet)
router.register(r'tags', StatusViewSet)
router.register(r'message', MessageViewSet)


urlpatterns = [
    url(
            r'',
                include(
                            router.urls,
                        ),
            ),
        ]
