from django.views.generic.edit import FormView
from .forms import RegistrantForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

@method_decorator(login_required, name='dispatch')
class Register(FormView):
    authentication_required = True
    template_name = 'register/registrant_form.html'
    form_class = RegistrantForm
    success_url = '/register/?event=Eggciting'

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
