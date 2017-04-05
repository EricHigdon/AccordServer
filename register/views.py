from django.views.generic.edit import FormView
from .models import Registrant
from .forms import RegistrantForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from .serializers import RegistrantSerializer
from django.shortcuts import get_object_or_404
from bulletin.models import Church
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@method_decorator(login_required, name='dispatch')
class Register(FormView):
    authentication_required = True
    template_name = 'register/registrant_form.html'
    form_class = RegistrantForm
    success_url = '/register/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            data = {}
            for item, value in self.request.GET.items():
                data[item] = value
            kwargs['initial'] = data
            kwargs['initial']['church'] = self.request.user.church.first()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

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
