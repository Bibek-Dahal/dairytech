
from dairyapp.models import FatRate, MilkRecord
import pytz
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives,get_connection
from django.core import mail
from datetime import datetime,date
def getShift():
    desired_timezone = pytz.timezone('Asia/Kathmandu')
    current_time = datetime.now(desired_timezone)
    print(current_time)


    # Extract the hour component from the current time
    current_hour = current_time.hour

    print("current_hour======",current_hour)

    # Determine whether it's AM or PM
    if current_hour < 12:

        return MilkRecord.shift_choices[0][0]
    else:
        return MilkRecord.shift_choices[1][0]

def sendMial(subject,to,from_email,filename,message=None,pdf=None):
    if not pdf:
        send_mail(
            subject=subject,
            message=message,
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

def getFatBasedOnDate(start_date,end_date):
    objs = FatRate.objects.all().order_by('-created_at')
    start_date_date = datetime.strptime(start_date, '%Y-%m-%d').date() 
    
    print("inside while")
    if start_date_date >= objs.first().created_at.date():
        return objs.first()
        
        
    return None
        
    

        