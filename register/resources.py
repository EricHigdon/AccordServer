from  import_export import resources, fields
from .models import Registrant, Child

class RegistrantResource(resources.ModelResource):
    children = fields.Field()

    def __init__(self, church, event, *args, **kwargs):
        if isinstance(church, int):
            self.church_id = church
        else:
            self.church_id = church.pk
        self.event = event
        return super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(church_id=self.church_id, event=self.event)

    def dehydrate_children(self, registrant):
        return ', '.join([str(child) for child in registrant.children.all()])

    class Meta:
        model = Registrant
        fields = (
            'event', 'first_name', 'last_name', 'email', 'phone', 'street1',
            'street2', 'city', 'state', 'zip_code'
        )
        export_order = (
            'event', 'first_name', 'last_name', 'email', 'phone', 'street1',
            'street2', 'city', 'state', 'zip_code', 'children'
        )
