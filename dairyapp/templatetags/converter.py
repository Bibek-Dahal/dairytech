from datetime import datetime
from django import template
from nepali.datetime import nepalidate
from nepali.datetime import nepalihumanize
register = template.Library()

from nepali.date_converter import converter

@register.filter
def convert_to_nepali(input_string):
    print("input string",input_string)
    input_string=input_string.strftime('%Y-%m-%d')
    date_format = "%Y-%m-%d"
    try:
        datetime.strptime(input_string, date_format)

        strippted_date = input_string.split('-')
        
        year,month,date = converter.english_to_nepali(int(strippted_date[0]), int(strippted_date[1]), int(strippted_date[2]))
        # return input_string
        np_date = nepalidate(year, month, date)
        # print(np_date.strftime("%B %d %Y"))
        output = nepalihumanize(np_date, threshold=1400)
        # print("output",output   )
        formatted_np_date = np_date.strftime("%B %d,%Y")
        return output
        # return f"{year}-{month}-{date}"


    except Exception as e:
        print(e)
        return False