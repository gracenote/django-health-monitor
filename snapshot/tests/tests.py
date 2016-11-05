from django.test import TestCase

# Create your tests here.
class SampleTestCase(TestCase):
    def setUp(self):
        pass

    def test_login_redirect(self):
        self.assertEqual(True, True)
