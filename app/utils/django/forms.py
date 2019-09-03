from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView


class FormMinxinView(FormMixin):
    def _init_data(self, view_type):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # Setting Model
        self.model = self.form.Meta.model

        # Setting Template
        self.template_name = f'{view_type}.html'


class FormListView(FormMinxinView, ListView):
    def get(self, request, *args, **kwargs):
        self._init_data('list')
        return super().get(request, *args, **kwargs)


class FormCreateView(FormMinxinView, CreateView):
    def get(self, request, *args, **kwargs):
        self._init_data('create')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._init_data('create')
        return super().post(request, *args, **kwargs)


class FormDetailView(FormMinxinView, DetailView):
    def get(self, request, *args, **kwargs):
        self._init_data('detail')
        return super().get(request, *args, **kwargs)


class FormUpdateView(FormMinxinView, UpdateView):
    success_redirect_with_kwargs = None

    def get(self, request, *args, **kwargs):
        self._init_data('update')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._init_data('update')
        self.success_url = reverse_lazy(self.success_redirect_with_kwargs, kwargs=kwargs)
        return super().post(request, *args, **kwargs)


class FormDeleteView(FormMinxinView, DeleteView):
    def get(self, request, *args, **kwargs):
        self._init_data('delete')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._init_data('delete')
        return super().post(request, *args, **kwargs)
