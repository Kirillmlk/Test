from django import forms
from mptt.forms import TreeNodeChoiceField
from .models import MenuItem


class MenuItemForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=MenuItem.objects.all())

    class Meta:
        model = MenuItem
        fields = ['name', 'url', 'named_url', 'parent']
