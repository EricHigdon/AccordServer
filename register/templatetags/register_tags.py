from django import template

register = template.Library()

@register.simple_tag
def render_field(form_field, css_classes=None):
    if css_classes is not None:
        existing_classes = form_field.field.widget.attrs.get('class', None)
        if existing_classes is not None:
            form_field.field.widget.attrs['class'] += ' ' + css_classes
        else:
            form_field.field.widget.attrs['class'] = css_classes

    return form_field
