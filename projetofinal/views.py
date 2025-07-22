from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView
from guardian.shortcuts import assign_perm

from projetofinal.decorators import management_required
from projetofinal.models import Equipe, Usuario, Projeto

@login_required
@management_required
def invite_user(request):
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            # Generate token and send email
            ...
    else:
        form = InviteForm()
    return render(request, 'invite.html', {'form': form})


"""@ratelimit(key='ip', rate='5/h')
    inserir login view aqui"""


class HomeView(TemplateView):
    template_name = "projetofinal/home.html"


class EquipeListView(ListView):
    model= Equipe
    template_name='projetofinal/equipes.html'
    context_object_name= 'equipes'




# Create your views here.
