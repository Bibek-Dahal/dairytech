from django import template 

register = template.Library()

@register.inclusion_tag('translate.html')
def google_translate(type="simple",language="en"):
    return {
        "language":language,
        "type":type
    }