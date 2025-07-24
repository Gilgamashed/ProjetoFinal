from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from guardian.shortcuts import assign_perm

from projetofinal.models import Usuario, Projeto, Convite

User = get_user_model()


class InvitationTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='admintest123'
        )
        self.client = Client()


def test_lead_permissions(self):
    lead = Usuario.objects.create_user(
        email='lead@test.com',
        password='test123',
        role='LEAD'
    )
    member = Usuario.objects.create_user(
        email='member@test.com',
        password='test123',
        role='MEMBER'
    )

    project = Projeto.objects.create(...)
    assign_perm('view_project', lead, project)

    self.assertTrue(lead.has_perm('view_project', project))
    self.assertFalse(member.has_perm('view_project', project))


def test_invite_creation(self):
    self.client.force_login(self.admin)
    response = self.client.post(reverse('send_invite'), {
        'email': 'newuser@test.com',
        'role': 'MEMBER'
    })
    self.assertEqual(response.status_code, 302)  # Should redirect
    self.assertTrue(Convite.objects.filter(email='newuser@test.com').exists())


def test_token_auto_generation(self):
    invite = Convite.objects.create(
        email='test@test.com',
        created_by=self.admin,
        role='MEMBER'
    )
    self.assertEqual(len(invite.token), 64)