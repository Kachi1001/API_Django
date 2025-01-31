from django.test import TransactionTestCase
from django.urls import reverse, include
from django.conf import settings
            
from django.db import models
from .routers import AppRouter

class URLConfigTestCase(TransactionTestCase):

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

    def test_db_for_read(self):
        router = AppRouter()

        # Cria um modelo fictício para teste
        class TestModel(models.Model):
            class Meta:
                app_label = 'lancamento_obra'

        # Verifica se o banco de dados correto é retornado
        self.assertEqual(router.db_for_read(TestModel), 'lancamento_obra')

    def test_allow_relation(self):
        router = AppRouter()

        # Cria objetos fictícios para teste
        class Obj1:
            _state = type('State', (), {'db': 'default'})

        class Obj2:
            _state = type('State', (), {'db': 'default'})

        # Verifica se a relação é permitida
        self.assertTrue(router.allow_relation(Obj1(), Obj2()))