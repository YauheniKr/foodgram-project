from django import template
from datetime import datetime, timedelta

register = template.Library()


@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60

    return f'{minutes}  min.'


@register.filter()
def convert_time_sec(td):
    if ':' in td:
        hours, minutes, seconds = td.split(':')
        recipe_duration = int((timedelta(
            hours=int(hours), minutes=int(minutes)).total_seconds() // 60))
        return recipe_duration
    return td


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter(name='parse_tags')
def parse_tags(get):
    return get.getlist('tag')


@register.filter(name='set_tag_qs')
def set_tag_qs(request, tag):
    new_req = request.GET.copy()
    tags = new_req.getlist('tag')

    if tag.title in tags:
        tags.remove(tag.title)
    else:
        tags.append(tag.title)

    new_req.setlist('tag', tags)
    return new_req.urlencode()
