import unittest
from app import app, db
from models import Subscription
from datetime import datetime


class SubscriptionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Настроим приложение для тестирования
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Временная база данных для тестов
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()  # Создаём таблицы перед запуском тестов

    @classmethod
    def tearDownClass(cls):
        # Удаляем таблицы после всех тестов
        with app.app_context():
            db.drop_all()

    def test_index_page(self):
        # Тест главной страницы
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"MY podpiski", response.data)

    def test_create_subscription(self):
        # Тест создания новой подписки
        response = self.client.post('/subscriptions/new', data={
            'name': 'Netflix',
            'amount': '15.99',
            'periodicity': 'monthly',
            'start_date': '2024-01-01'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Netflix", response.data)
        self.assertIn(b"15.99", response.data)
        self.assertIn(b"monthly", response.data)

    def test_edit_subscription(self):
        # Создаём подписку для теста редактирования
        with app.app_context():
            subscription = Subscription(
                name='Spotify',
                amount=9.99,
                periodicity='monthly',
                start_date=datetime(2024, 1, 1).date()
            )
            db.session.add(subscription)
            db.session.commit()
            subscription_id = subscription.id

        # Редактируем подписку
        response = self.client.post(f'/subscriptions/edit/{subscription_id}', data={
            'name': 'Spotify Premium',
            'amount': '12.99',
            'periodicity': 'monthly',
            'start_date': '2024-01-01'
        }, follow_redirects=True)

        # Проверяем, что данные обновились в ответе
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Spotify Premium", response.data)
        self.assertIn(b"12.99", response.data)

        # Дополнительно проверяем, что данные в базе данных обновились
        with app.app_context():
            updated_subscription = Subscription.query.get(subscription_id)
            self.assertEqual(updated_subscription.name, 'Spotify Premium')
            self.assertEqual(updated_subscription.amount, 12.99)

    def test_delete_subscription(self):
        # Создаём подписку для теста удаления
        with app.app_context():
            subscription = Subscription(
                name='YouTube Premium',
                amount=11.99,
                periodicity='monthly',
                start_date=datetime(2024, 1, 1).date()
            )
            db.session.add(subscription)
            db.session.commit()
            subscription_id = subscription.id

        # Удаляем подписку
        response = self.client.get(f'/subscriptions/delete/{subscription_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"YouTube Premium", response.data)

        # Проверяем, что подписка была удалена из базы данных
        with app.app_context():
            deleted_subscription = Subscription.query.get(subscription_id)
            self.assertIsNone(deleted_subscription)


if __name__ == '__main__':
    unittest.main()

