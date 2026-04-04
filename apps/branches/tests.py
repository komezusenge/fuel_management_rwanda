from django.test import TestCase
from apps.branches.models import Branch


class BranchModelTest(TestCase):
    def test_create_branch(self):
        branch = Branch.objects.create(
            name='Musanze Branch',
            location='Musanze, Northern Province',
            phone='+250788000001',
        )
        self.assertEqual(branch.name, 'Musanze Branch')
        self.assertTrue(branch.is_active)
        self.assertIn('Musanze Branch', str(branch))

    def test_branch_ordering(self):
        Branch.objects.create(name='Zulu Branch', location='Kigali')
        Branch.objects.create(name='Alpha Branch', location='Huye')
        branches = list(Branch.objects.all())
        self.assertEqual(branches[0].name, 'Alpha Branch')
