import json
from django.http import JsonResponse

class JsonableResponseMixin:
    """
    Mixin para suportar requisições JSON (ideal para chamadas AJAX/API
    combinando com as CBVs genéricas de formulário
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)

        if self.request.get_preferred_type(['text/html', 'application/json']) == 'text/html':
            return response

        # Senão, responde erros via JSON
        return JsonResponse(form.error, status=400)

    def form_valid(self, form):
        response = super().form.valid(form)