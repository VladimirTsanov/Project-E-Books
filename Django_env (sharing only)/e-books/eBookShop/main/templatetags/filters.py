# yourapp/templatetags/filters.py
from django import template
from urllib.parse import parse_qs, urlencode

register = template.Library()

@register.filter
def update_param(query_string, args):
    key, val = args.split(',')
    params = parse_qs(query_string)
    params[key] = [val]
    return urlencode(params, doseq=True)

@register.filter
def remove_param(query_string, key):
    params = parse_qs(query_string)
    params.pop(key, None)
    return urlencode(params, doseq=True)

@register.filter
def remove_one_val(query_string, args):
    if ',' not in args:
        return ''  # връщаме празен string при грешни аргументи
    key, val = args.split(',', 1)
    params = parse_qs(query_string)
    if key in params:
        params[key] = [v for v in params[key] if v != val]
        if not params[key]:
            params.pop(key)
    return urlencode(params, doseq=True)

@register.filter
def remove_price_params(query_string):
    params = parse_qs(query_string)
    params.pop("min_price", None)
    params.pop("max_price", None)
    return urlencode(params, doseq=True)

@register.filter
def get_title(genres, id):
    return genres.get(id=id).title

@register.filter
def get_name(authors, id):
    return authors.get(id=id).name

@register.simple_tag
def build_query(request, remove_key=None, remove_val=None):
    params = request.GET.copy()

    if remove_key and remove_val:
        values = params.getlist(remove_key)
        remove_val = str(remove_val)
        if remove_val in values:
            values.remove(remove_val)
        if values:
            params.setlist(remove_key, values)
        else:
            params.pop(remove_key, None)

    elif remove_key:
        params.pop(remove_key, None)

    return params.urlencode()
