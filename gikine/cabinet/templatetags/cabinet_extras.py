from django import template
import calendar

register = template.Library()

@register.filter(name='format_mois')
def format_mois(value):
    
    return calendar.month_name[int(value)]

@register.filter
def get_item(dictionary, key):
    return dictionary.get(f"annee_{key}")