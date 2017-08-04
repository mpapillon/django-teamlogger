from django import template
from django.forms import BoundField, Select, Form, RadioSelect, CheckboxSelectMultiple, CheckboxInput, TextInput, \
    Textarea, PasswordInput
from django.template.loader import get_template

register = template.Library()


def add_class(field, *classes):
    css_classes = field.field.widget.attrs.get('class', None)

    if css_classes:
        css_classes = css_classes.split(' ')
    else:
        css_classes = []

    for clazz in [c for c in classes if c not in css_classes]:
        css_classes.append(clazz)

    return field.as_widget(attrs={'class': ' '.join(css_classes)})


@register.filter
def input_type(field):
    widget = field.field.widget

    if isinstance(widget, TextInput) or isinstance(widget, Textarea):
        return 'text'
    if isinstance(widget, PasswordInput):
        return 'password'
    if isinstance(widget, CheckboxInput):
        return 'checkbox'
    if isinstance(widget, CheckboxSelectMultiple):
        return 'multicheckbox'
    if isinstance(widget, RadioSelect):
        return 'radioset'
    if isinstance(widget, Select):
        return 'choice'

    return 'default'


@register.filter
def to_spectre_field(field, size=None):
    field_type = input_type(field)

    if field_type == 'text' or field_type == 'password':
        if size:
            size_class = 'input-%s' % size
            field = add_class(field, 'form-input', size_class)
        else:
            field = add_class(field, 'form-input')
    elif field_type == 'choice':
        if size:
            size_class = 'select-%s' % size
            field = add_class(field, 'form-select', size_class)
        else:
            field = add_class(field, 'form-select')

    return field


@register.filter
def as_spectre(form_or_field, size=None, layout=None):
    """
    Render a form or a field with Spectre.css guidelines.
    :param form_or_field:
    :param size:
    :param layout:
    :return:
    """
    if isinstance(form_or_field, BoundField):
        return get_template("spectre/field.html").render({
            'field': form_or_field,
            'size': size,
        })
    elif isinstance(form_or_field, Form):
        return get_template("spectre/form.html").render({
            'form': form_or_field,
            'size': size,
        })
    else:
        return form_or_field
