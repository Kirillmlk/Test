from django import template
from django.shortcuts import render
from .models import MenuItem

from django.http import HttpResponse


def menu(request):
    menu_items = MenuItem.objects.all()
    context = {
        'menu_items': menu_items,
    }
    return render(request, 'menu.html', context)


def my_view(request):
    return HttpResponse("Privet")


register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, name):
    menu_items = MenuItem.objects.filter(name=name).get_descendants(include_self=True)

    request = context.get('request')
    current_path = request.path
    current_item = None
    for item in menu_items:
        if item.url and item.url == current_path:
            current_item = item
            break
        elif item.named_url and request.resolver_match and item.named_url == request.resolver_match.url_name:
            current_item = item
            break

    return render(context['request'], 'menu_app/menu.html', {'menu_items': menu_items, 'current_item': current_item})