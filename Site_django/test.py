# tests.py
from django.test import TestCase
from django.urls import reverse, include
from django.conf import settings


class URLConfigTestCase(TestCase):

    def test_status_url(self):
        # Testa se a URL "/status" responde corretamente
        response = self.client.get(reverse('status'))
        self.assertEqual(response.status_code, 200)

    def test_missing_url_in_app(self):
        errors = []
        for app in settings.INTERNAL_APP:
            try:
                # Tenta incluir as URLs do app
                include(f"{app}.urls")
            except Exception as e:
                # Usa assertTrue para falhar sem traceback
                errors.append(f"\nO carregamento das URLs falhou para o app {app}. Erro: {str(e)}")

        if errors:
            self.fail(''.join(errors))
