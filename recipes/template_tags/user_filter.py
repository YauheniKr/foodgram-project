from django import template

register = template.Library()


@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())
    minutes = (total_seconds % 3600) // 60

    return f'{minutes}  min.'
