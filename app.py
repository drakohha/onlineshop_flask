from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Произошла ошибка"

    else:
        return render_template('create.html')


@app.route('/bay', methods=['POST', 'GET'])
def bay():
    item = Item.query.all()
    try:
        api = Api(merchant_id=1396424,
                  secret_key='test',
                  request_type='xml',
                  api_protocol='1.0',
                  api_domain='api.fondy.eu')  # json - is default
        checkout = Checkout(api=api)
        data = {
            "preauth": 'Y',
            "currency": "RUB",
            "amount": 10000,
            "reservation_data": {
                'test': 1,
                'test2': 2
            }
        }
        response = checkout.url(data)
        return redirect('/')
    except:
        return "Произошла ошибка c платежной системой"

    return render_template('bay.html' ,data=item)


if __name__ == '__main__':
    app.run(debug=True)
