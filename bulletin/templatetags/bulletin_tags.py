from django import template
from datetime import datetime

register = template.Library()

@register.assignment_tag
def date(date_string):
    date = datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S +0000")
    return date
