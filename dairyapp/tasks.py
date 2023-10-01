from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives,get_connection
from celery import shared_task
from django.template.loader import render_to_string

@shared_task
def sendMial(subject,to,from_email,filename,message=None,pdf=None):
    if not pdf:
        send_mail(
            subject=subject,
            message="message",
            from_email=from_email,
            recipient_list=[to],
            fail_silently=False,
        )

    if pdf:
        print("inside pdf view========")
        subject, from_email, to = subject, from_email, to
        text_content = "This is an important message."
        html_content = render_to_string('dairyapp/email/email_format.html')
        msg = EmailMultiAlternatives(subject=subject,from_email=from_email,to= [to])
        mimetype_pdf = 'application/pdf'
        msg.attach(filename, pdf, mimetype_pdf)
        msg.attach_alternative(html_content, "text/html")
       
        msg.send(fail_silently=False)

@shared_task
def add(x, y):
    return x + y