from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items = Item.query.order_by(Item.title).all()
    return render_template('index.html', items=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        amount = request.form['amount']
        price = request.form['price']
        item = Item(title=title, text=text, amount=amount, price=price)


        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Произашла ошибка"

    else:
        return render_template('create.html')

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

if __name__ == '__main__':
    app.run(debug=True)