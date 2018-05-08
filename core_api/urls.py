from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'support', SupportViewset)
router.register(r'network', RepairNetworkViewset)
router.register(r'customer', CustomerViewset)

urlpatterns = [
    url(
            r'^',
                include(
                            router.urls,
                        ),
            ),
        ]
