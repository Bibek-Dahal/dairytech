
from dairyapp.models import FatRate, MilkRecord
import pytz
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives,get_connection
from django.core import mail
from datetime import datetime,date

from nepali.date_converter import converter
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
    print(objs.first())
    if objs and (start_date_date >= objs.first().created_at.date()):
        return objs.first()
        
        
    return None

from datetime import datetime

def is_valid_date(input_string):
    date_format = "%Y-%m-%d"
    try:
        datetime.strptime(input_string, date_format)

        
        return input_string

    except Exception as e:
        print(e)
        return False
    
def convert_nepali_date(input_string):
    date_format = "%Y-%m-%d"
    try:
        datetime.strptime(input_string, date_format)

        strippted_date = input_string.split('-')
        print("----------",strippted_date)
        print("00000000000",converter.nepali_to_english(int(strippted_date[0]), int(strippted_date[1]), int(strippted_date[2])))
        year,month,date = converter.nepali_to_english(int(strippted_date[0]), int(strippted_date[1]), int(strippted_date[2]))
        # return input_string
        if month<10:
            return f"{year}-0{month}-{date}"
        return f"{year}-{month}-{date}"
    except Exception as e:
        print(e)
        return False

        
    

        