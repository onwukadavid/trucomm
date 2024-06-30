from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def full_url(context, **kwargs):
    query_string = context['request'].GET.copy()
    for k,v in kwargs.items():
        query_string[k] = v
    return query_string.urlencode()