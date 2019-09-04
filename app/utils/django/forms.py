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
        if not self.template_name:
            self.template_name = f'{self.model._meta.app_label}/{view_type}.html'


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
    view_name = None

    def get(self, request, *args, **kwargs):
        self._init_data('update')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._init_data('update')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        if self.view_name:
            self.success_url = reverse_lazy(self.view_name, kwargs=self.kwargs)
        else:
            self.success_url = super().get_success_url()
        return str(self.success_url)


class FormDeleteView(FormMinxinView, DeleteView):
    def get(self, request, *args, **kwargs):
        self._init_data('delete')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._init_data('delete')
        return super().post(request, *args, **kwargs)
