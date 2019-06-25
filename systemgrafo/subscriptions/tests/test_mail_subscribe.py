from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Fabio Freire', cpf='12345678901', email='fabio.araujo@soulasalle.com.br',
                    phone='21-99999-9999')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@systemgrafo.com.br'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@systemgrafo.com.br', 'fabio.araujo@soulasalle.com.br']

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Fabio Freire',
            '12345678901',
            'fabio.araujo@soulasalle.com.br',
            '21-99999-9999',
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
        # self.assertIn('Fabio Freire', self.email.body)
        # self.assertIn('12345678901', self.email.body)
        # self.assertIn('fabio.araujo@soulasalle.com.br', self.email.body)
        # self.assertIn('21-99999-9999', self.email.body)