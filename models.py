from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Subscription(db.Model):
    __tablename__ = 'Subscription'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    periodicity = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    next_payment_date = db.Column(db.Date, nullable=False)

    def __init__(self, name, amount, periodicity, start_date):
        self.name = name
        self.amount = amount
        self.periodicity = periodicity
        self.start_date = start_date
        # Расчет следующей даты платежа
        self.next_payment_date = self.calculate_next_payment_date(start_date, periodicity)

    def calculate_next_payment_date(self, start_date, periodicity):
        """ Рассчитываем следующую дату списания в зависимости от периодичности """
        if periodicity == 'monthly':
            return start_date.replace(month=start_date.month % 12 + 1)
        elif periodicity == 'yearly':
            return start_date.replace(year=start_date.year + 1)
        else:
            # Для других типов периодичности можно добавить дополнительные условия
            return start_date

    def to_dict(self):
        """ Метод для преобразования объекта в словарь для API """
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'periodicity': self.periodicity,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'next_payment_date': self.next_payment_date.strftime('%Y-%m-%d')
        }

