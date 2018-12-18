from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from ..serializers.ticket import TicketSerializer
from ..serializers.chain import ChatSerializer
from ..pagination import LargeResultsSetPagination

class TicketViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketSerializer
    queryset = serializer_class.Meta.model.objects.all()
    pagination_class = LargeResultsSetPagination

    def retrieve(self,request,pk=None):
        ticket = self.get_object()
        chat = ChatSerializer(instance=ticket.chat)
        ticket = TicketSerializer(instance=ticket)

        data = ticket.data
        data['chat'] = chat.data
        return Response(data)

    def list(self, request):
        try:
            pk = request.GET.get('pk','')
            self.queryset = self.queryset.filter(support=pk)
        except:
            pass
        return super(TicketViewset, self).list(request, *args, **kwargs)
