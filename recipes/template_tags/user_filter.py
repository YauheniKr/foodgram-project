from django import template
from datetime import datetime, timedelta

from recipes.models import Follow, Favorite

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


@register.filter
def conjoin(number, args):
    args = [arg.strip() for arg in args.split(',')]
    last_digit = int(number) % 10
    if last_digit == 1:
        return f'{number} {args[0]}'
    elif 1 < last_digit < 5:
        return f'{number} {args[1]}'
    elif last_digit > 4 or last_digit == 0:
        return f'{number} {args[2]}'


@register.filter
def is_subscribed_to(user, author):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter
def tags_to_url_params(tags):
    return '&' + '&'.join([f'tag={tag}' for tag in tags])


@register.filter
def is_favored_by(recipe, user):
    return Favorite.objects.filter(recipe=recipe, user=user).exists()
