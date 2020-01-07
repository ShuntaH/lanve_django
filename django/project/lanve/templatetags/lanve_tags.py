from django import template

register = template.Library()


@register.filter(name='ratio')
def ratio(value1, value2):
    if value1 + value2 == 0:
        return 0
    else:
        return value1/(value1 + value2)
