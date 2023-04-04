from django import template
from django.urls import reverse

from menu_app.models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path_info
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')
    menu = []
    for item in menu_items:
        if not item.parent:
            menu.append({'title': item.title, 'url': reverse(item.url_name) if item.url_name else item.url,
                         'children': [], 'active': current_path.startswith(item.url)})
        else:
            for menu_item in menu:
                if item.parent == menu_item.get('id'):
                    menu_item['children'].append(
                        {'title': item.title, 'url': reverse(item.url_name) if item.url_name else item.url,
                         'active': current_path.startswith(item.url)})
                    break
    return template.loader.render_to_string('menu_app/menu.html', {'menu': menu})