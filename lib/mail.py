from django.core.mail import EmailMessage, EmailMultiAlternatives

# data = {'subject':'Fixed price repair booking',
#         'body': render('response.html'),
#         'to': 'vex@vex.com',
#        }

def send_engineer_mail(engineer_email, data):
    email = EmailMultiAlternatives(data['subject'], data['body'], to=[enginer_email])
    email.attach_alternative(data['html'], 'text/html')

    email.send()

def send_mail_to_customer(customer_email, data):
    email = EmailMultiAlternatives(data['subject'], data['body'], to=[customer_email])
    email.attach_alternative(data['html'], 'text/html')

    email.send()

# tasks once a week
def send_commercial_mails():
    pass

def send_weekly_digest():
    pass
