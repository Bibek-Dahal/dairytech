
from dairyapp.models import FatRate, MilkRecord
import pytz
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives,get_connection
from django.core import mail
from datetime import datetime,date
from django.contrib import messages
from nepali.date_converter import converter
from django.utils.translation import gettext_lazy as _
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

def getFatBasedOnDate(start_date,end_date,dairy,req):
    print("dairy%%%%%%%%%%%%",dairy)
    objs = FatRate.objects.filter(dairy__user=req.user,dairy=dairy).order_by('-created_at')
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
        # print("----------",strippted_date)
        # print("00000000000",converter.nepali_to_english(int(strippted_date[0]), int(strippted_date[1]), int(strippted_date[2])))
        year,month,date = converter.nepali_to_english(int(strippted_date[0]), int(strippted_date[1]), int(strippted_date[2]))
        # return input_string
        # print(f"year {year} month {month} date {date}")
        if month<10:
            return f"{year}-0{month}-{date}"
        return f"{year}-{month}-{date}"
    

    except Exception as e:
        print(e)
        return False


def get_fat_rate_fun(self,start_date,end_date,dairy,fat_rate_obj):
    print("inside get fat rate========")
        
    try:


        """
            New Logic
        """
        if fat_rate_obj.count()>1:
            #raise error if multiple fat range exists within date range
            messages.error(self.request, _("Cannot apply filter witin date range. Multiple fat rate exists."))
            return 0
        elif fat_rate_obj.count() == 1:
            fat_rate = fat_rate_obj.first().get_fat_rate
            self.kwargs['fat_rate'] = fat_rate_obj.first().fat_rate
            self.kwargs['bonous'] = fat_rate_obj.first().bonous_amount
            self.kwargs['total_fat_rate'] = fat_rate
            print("fat rate===",fat_rate)
            # return fat_rate
            return {
                'fat_rate':fat_rate,
                'fat_rate_obj':fat_rate_obj.first()
            }

        elif getFatBasedOnDate(start_date,end_date,dairy,self.request) is not None:
            
            print("inside first elif")
            fat_rate_obj = getFatBasedOnDate(start_date,end_date,dairy,self.request)
            fat_rate = fat_rate_obj.get_fat_rate
            self.kwargs['fat_rate'] = fat_rate_obj.fat_rate
            self.kwargs['bonous'] = fat_rate_obj.bonous_amount
            self.kwargs['total_fat_rate'] = fat_rate
            return {
                'fat_rate':fat_rate,
                'fat_rate_obj':fat_rate_obj
            }

        elif FatRate.objects.filter(dairy=dairy,dairy__user=self.request.user).order_by("created_at").exists():
            fat_rate_obj = FatRate.objects.filter(dairy=dairy,dairy__user=self.request.user).order_by("created_at").first()
            fat_rate = fat_rate_obj.get_fat_rate
            self.kwargs['fat_rate'] = fat_rate_obj.fat_rate
            self.kwargs['bonous'] = fat_rate_obj.bonous_amount
            self.kwargs['total_fat_rate'] = fat_rate
            return {
                'fat_rate':fat_rate,
                'fat_rate_obj':fat_rate_obj.first()
            }
        else:
            print("inside last else")
            messages.error(self.request, _("Cannot fint fat rate witin date range.Fat rate doesnot exists."))
            self.kwargs['fat_rate'] = 0
            self.kwargs['bonous'] = 0
            self.kwargs['total_fat_rate'] = 0
            return 0
    except Exception as e:
        print("exception occour")
        return 0
        
    

        