import secrets
from datetime import timezone, timedelta

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from projetofinal.constants import CATEGORIA, STATUS, PRIORIDADE, HIERARCH


class Usuario(AbstractUser):

    username = None
    email = models.EmailField(_('email'), unique=True, db_index=True)

    #Pessoal
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)

    #Auth
    is_verified = models.BooleanField(_('verified'), default=False)

    USERNAME_FIELD = 'email'  # Usar email como login
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Pro createsuperuser

    role = models.CharField(
        max_length=20,
        choices=HIERARCH,
        default='MEMBER'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',  # Unique name?
        blank=True,
        verbose_name=_('groups'),
        help_text=_('The groups this user belongs to...'),
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_set',  # Also make this unique?
        blank=True,
        verbose_name=_('user permissions'),
        help_text=_('Specific permissions for this user...'),
    )

    def __str__(self):
        return f"{self.email} - Acesso: {self.get_role_display()}"

class Convite(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=50, unique=True, editable=False)
    role = models.CharField(max_length=20, choices=HIERARCH)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    accepted = models.BooleanField(default=False)
    expires = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite for {self.email} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(32)  # random token
        if not self.expires:
            self.expires = timezone.now() + timedelta(days=3)  # 3 dias
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('accept_invite', kwargs={'token': self.token})

    def is_expired(self):
        return timezone.now() > self.expires



class Equipe(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    membros = models.ManyToManyField(Usuario)

    def __str__(self):
        return f"{self.nome}"

class Projeto(models.Model):
    name = models.CharField(max_length=200)
    criador = models.ForeignKey(User, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True)
    categoria = models.CharField(max_length=100, choices=CATEGORIA)
    inicio = models.DateField()
    prazofinal = models.DateField()


class Tarefa(models.Model):
    tarefa = models.CharField(max_length=200)
    descricao = models.TextField()
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=15, choices=STATUS, default='parafazer')
    prazofinal = models.DateField()
    inicio = models.DateField(auto_now_add=True)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE)

    def __str__(self):
        return f"{self.tarefa} - {self.status} - {self.prazo}"

class AuditLog(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)       #o que ocorreu
    onde = models.CharField(max_length=100)         #aonde ocorreu a mudança
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)


# Create your models here.
