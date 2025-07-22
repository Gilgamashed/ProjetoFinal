from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import PermissionDenied


class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # Desabilita signup publico
        return False

    def save_user(self, request, user, form, commit=True):
        # Registro apenas por convite de admin
        if not request.user.is_staff:
            raise PermissionDenied("Por favor, entre em contato com um admin para criação de uma Account")
        return super().save_user(request, user, form, commit)