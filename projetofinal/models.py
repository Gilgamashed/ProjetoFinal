import secrets
from datetime import timezone, timedelta

from django.contrib.auth.models import User, AbstractUser
from django.db import models

from projetofinal.constants import CATEGORIA, STATUS, PRIORIDADE, HIERARCH


class Usuario(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',  # Unique name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to...',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_set',  # Also make this unique
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user...',
    )

    def __str__(self):
        return f"{self.nome} - {self.cargo} - Acesso {self.role}"

class Convite(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=10, choices=HIERARCH)
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
