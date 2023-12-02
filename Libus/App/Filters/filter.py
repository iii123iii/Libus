from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def ImgFilter(value):
    if(value.endswith(".png") or value.endswith(".jpg") or value.endswith(".webp")):
        return "img"
    elif(value.endswith(".mp4")):
        return "video/mp4"
    else:
        return "n"
    
