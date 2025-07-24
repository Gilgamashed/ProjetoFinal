from datetime import timezone

from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import PermissionDenied

from projetofinal.models import Convite


class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # Desabilita signup publico
        return False

    def save_user(self, request, user, form, commit=True):
        # Registro apenas por convite de admin
        if not request.user.is_staff:
            raise PermissionDenied("Por favor, entre em contato com um admin para criação de sua conta")
        return super().save_user(request, user, form, commit)

    def clean_email(self, email):
        # checa se email tem convite ativo
        if not Convite.objects.filter(
            email__iexact=email,
            is_accepted=False,
            expires_at__gt=timezone.now()
        ).exists():
            raise PermissionDenied("Nenhum convite foi encontrado para este e-mail")
        return email