from django.test import TestCase
from guardian.shortcuts import assign_perm

from projetofinal.models import Usuario, Projeto


class PermissionTests(TestCase):
    def test_lead_permissions(self):
        lead = Usuario.objects.create(role='LEAD')
        member = Usuario.objects.create(role='MEMBER')
        project = Projeto.objects.create(...)

        assign_perm('view_project', lead, project)
        self.assertTrue(lead.has_perm('view_project', project))
        self.assertFalse(member.has_perm('view_project', project))