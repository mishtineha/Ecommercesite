from django import template

register = template.Library()

@register.filter
def get_initials(name):
    name = name.split(" ")
    try:
        initial = name[0][0]
        if len(name) > 1:
            initial += name[1][1]
    except:
        initial = ""
    return initial