from flask import Flask, render_template, request, redirect, url_for
from models import db, Subscription
from datetime import datetime

app = Flask(__name__)

user_db = "alex2003"
host_ip ="127.0.0.1"
host_port = "5432"
database_name = "RGZ1"
password = "1234"

# Настройка подключения к базе данных PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    subscriptions = Subscription.query.all()
    return render_template('index.html', subscriptions=subscriptions)

@app.route('/subscriptions/new', methods=['GET', 'POST'])
def create_subscription():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        periodicity = request.form['periodicity']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()

        new_subscription = Subscription(
            name=name,
            amount=amount,
            periodicity=periodicity,
            start_date=start_date
        )
        db.session.add(new_subscription)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create_subscription.html')

@app.route('/subscriptions/edit/<int:id>', methods=['GET', 'POST'])
def edit_subscription(id):
    subscription = Subscription.query.get(id)
    if request.method == 'POST':
        subscription.name = request.form['name']
        subscription.amount = request.form['amount']
        subscription.periodicity = request.form['periodicity']
        subscription.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        subscription.next_payment_date = subscription.calculate_next_payment_date(subscription.start_date, subscription.periodicity)
        
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_subscription.html', subscription=subscription)

@app.route('/subscriptions/delete/<int:id>', methods=['GET'])
def delete_subscription(id):
    subscription = Subscription.query.get(id)
    if subscription:
        db.session.delete(subscription)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаёт таблицы в базе данных при первом запуске
    app.run(debug=True)
