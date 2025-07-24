from allauth.account.forms import SignupForm
from django import forms

from projetofinal.models import Convite

class ConviteForm(forms.ModelForm):
    class Meta:
        model = Convite
        fields = ['email', 'role']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Convite.objects.filter(email__iexact=email, is_accepted=False).exists():
            raise forms.ValidationError("Já existe um convite pendente pra esse email.")
        return email


class ConviteSignupForm(SignupForm):
    invite_token = forms.CharField(widget=forms.HiddenInput(), required=False)

    def save(self, request):
        user = super().save(request)

        #Processar convite
        token = self.cleaned_data.get('invite_token')
        if token:
            try:
                invite = Convite.objects.get(token=token)
                invite.is_accepted = True
                invite.save()
                user.role = invite.role
                user.save()
            except Convite.DoesNotExist:
                pass

        return user

