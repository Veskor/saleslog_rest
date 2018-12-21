from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from django.template.loader import render_to_string

from lib.mail import send_mail_to_customer, send_engineer_mail

class MailSender(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        pass
        # return a list of mail endpoints or something like that

    @detail_route(methods=['post'])
    def mail_customer(self, request, pk):

        mail_case = request.POST['case']

        data = dict()

        if mail_case == 'fpr':
            data['subject'] = 'Fixed price repair booking'
            data['body'] = 'some text'
            data['html'] = render_to_string('response.html')
        elif mail_case == 'abc'
            pass
        else:
            pass


    @detail_route(methods=['post'])
    def mail_engineer(self, request, pk):

        mail_case = request.POST['case']
