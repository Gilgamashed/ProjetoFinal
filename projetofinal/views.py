from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, TemplateView
from guardian.shortcuts import assign_perm

from config import settings
from projetofinal.decorators import management_required
from projetofinal.forms import ConviteForm
from projetofinal.models import Equipe, Usuario, Projeto, Convite


@login_required
@management_required
def invite_user(request):
    if request.method == 'POST':
        form = ConviteForm(request.POST)
        if form.is_valid():
            invite = form.save(commit=False)
            invite.created_by = request.user
            invite.save()

            #Manda o email
            accept_url = request.build_absolute_uri(invite.get_absolute_url())
            send_mail(
                subject = f"Convite para {settings.SITE_NAME}",
                message = f"""Você recebeu um convite para ingressar {settings.SITE_NAME} como {invite.get_role_display()}!

                        Acesse esse link para aceitar seu convite: {accept_url}
                        
                        Esse link tem validade até {invite.expires.strftime('%Y-%m-%d')}""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[invite.email],
            )
            return redirect('invite_sent')
    else:
        form = ConviteForm()
    return render(request, 'account/send_invite', {'form': form})

def accept_invite(request,token):
    try:
        invite = Convite.objects.get(token=token, is_accepted=False)
    except Convite.DoesNotExist:
        return render(request, 'account/invite_error.html')

    # preenche email no form de sign up
    signup_url = reverse('account_signup') + f'?email={invite.email}'
    return redirect(signup_url)


"""@ratelimit(key='ip', rate='5/h')
    inserir login view aqui"""


class HomeView(TemplateView):
    template_name = "projetofinal/home.html"


class EquipeListView(ListView):
    model= Equipe
    template_name='projetofinal/equipes.html'
    context_object_name= 'equipes'




# Create your views here.
