from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')  # Add this line

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')  # Add this line

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')

    __table_args__ = (
        CheckConstraint('price >= 1 AND price <= 30', name='check_price_range'),
    )


# GET all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_list = [{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants]
    return jsonify(restaurant_list)


# GET restaurant by ID
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        # pizza_list = [{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in restaurant.pizzas]
        restaurant_info = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            # 'pizzas': pizza_list
        }
        return jsonify(restaurant_info)
    else:
        return jsonify({'error': 'Restaurant not found'}), 404


# DELETE restaurant by ID
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        # Delete associated RestaurantPizzas
        for rp in restaurant.restaurant_pizzas:
            db.session.delete(rp)
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': 'Restaurant not found'}), 404


# GET all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_list = [{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in pizzas]
    return jsonify(pizza_list)


# POST a new RestaurantPizza
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    # Validate data
    if not (1 <= price <= 30):
        return jsonify({'errors': ['Validation error: Price must be between 1 and 30']}), 400

    restaurant = Restaurant.query.get(restaurant_id)
    pizza = Pizza.query.get(pizza_id)

    if not (restaurant and pizza):
        return jsonify({'errors': ['Validation error: Restaurant or Pizza not found']}), 400

    restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
    db.session.add(restaurant_pizza)
    db.session.commit()

    return jsonify({'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}), 201


if __name__ == '__main__':
    app.run(debug=True)
