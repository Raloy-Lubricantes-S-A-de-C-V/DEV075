from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
@register.filter
def get_class(value):
        classes = value.field.widget.attrs.get('class', '').split(' ')
        return classes[1]

@register.filter
def get_class2(value):
        classes = value.field.widget.attrs.get('class', '').split(' ')
        return classes[2]