from django.views.generic.edit import FormView
from .models import Registrant
from .forms import RegistrantForm, ChildrenFormSet
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from .serializers import RegistrantSerializer
from django.shortcuts import get_object_or_404
from bulletin.models import Church
from django.views.generic import CreateView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@method_decorator(login_required, name='dispatch')
class Register(CreateView):
    authentication_required = True
    template_name = 'register/registrant_form.html'
    form_class = RegistrantForm
    success_url = '/register/'

    def get_forms(self, post=False):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if self.request.GET.get('children', False):
            if self.request.method == 'POST':
                children_form = ChildrenFormSet(self.request.POST)
            else:
                children_form = ChildrenFormSet()
        else:
            children_form = None
        return form, children_form

    def get(self, request, *args, **kwargs):
        form, children_form = self.get_forms()
        return self.render_to_response(
            self.get_context_data(form=form, children_form=children_form)
        )

    def post(self, request, *args, **kwargs):
        form, children_form = self.get_forms(post=True)
        forms_valid = True
        if not form.is_valid():
            forms_valid = False
        if children_form is not None and not children_form.is_valid():
            forms_valid = False
        if forms_valid:
            return self.form_valid(form, children_form)
        else:
            return self.form_invalid(form, children_form)

    def form_valid(self, form, children_form):
        self.object = form.save()
        if children_form is not None:
            children_form.instance = self.object
            children_form.save()
        return super().form_valid(form)

    def form_invalid(self, form, children_form):
        return self.render_to_response(
            self.get_context_data(form=form, children_form=children_form)
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            data = {}
            for item, value in self.request.GET.items():
                data[item] = value
            kwargs['initial'] = data
            kwargs['initial']['church'] = self.request.user.church.first()
        return kwargs

    def get_success_url(self):
        return self.request.build_absolute_uri()

class RegistrantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows slides to be viewed.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Registrant.objects.order_by('-pk')
    serializer_class = RegistrantSerializer

    def get_queryset(self):
        church = get_object_or_404(Church, admins=self.request.user)
        event = self.request.GET.get('event', '')
        return church.registrants.filter(
            event=event
        ).order_by('-pk')
